import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random
import numpy as np

class JigsawPuzzleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Jigsaw Puzzle Game")

        self.canvas_width = 1200  # Adjust canvas width
        self.canvas_height = 600  # Adjust canvas height
        self.piece_size = 200  # Adjust puzzle piece size

        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.load_button = tk.Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.shuffle_button = tk.Button(master, text="Shuffle Pieces", command=self.shuffle_pieces)
        self.shuffle_button.pack()

        self.image_path = None
        self.original_image = None
        self.pieces = []

    def load_image(self):
        self.image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.create_puzzle_pieces()

    def create_puzzle_pieces(self):
        self.canvas.delete("all")
        self.pieces.clear()

        # Create a blank tile as the first piece
        blank_image = Image.new("RGB", (self.piece_size, self.piece_size), "white")
        self.pieces.append(PuzzlePiece(self.canvas, blank_image, 0, 0, self.piece_size))

        # Resize the image to fit the canvas
        resized_image = self.original_image.resize((self.canvas_width, self.canvas_height))

        # Divide the resized image into puzzle pieces
        for y in range(self.canvas_height // self.piece_size):
            for x in range(self.canvas_width // self.piece_size):
                left = x * self.piece_size
                top = y * self.piece_size
                right = left + self.piece_size
                bottom = top + self.piece_size
                piece_image = resized_image.crop((left, top, right, bottom))
                piece = PuzzlePiece(self.canvas, piece_image, x + 1, y, self.piece_size)
                self.pieces.append(piece)

    def shuffle_pieces(self):
        random.shuffle(self.pieces)
        for i, piece in enumerate(self.pieces):
            piece.grid_x = i % (self.canvas_width // self.piece_size)
            piece.grid_y = i // (self.canvas_width // self.piece_size)
            piece.update_position()

class PuzzlePiece:
    def __init__(self, canvas, image, grid_x, grid_y, piece_size):
        self.canvas = canvas
        self.image = ImageTk.PhotoImage(image)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.piece_size = piece_size
        self.piece_id = None

        self.create_piece()

    def create_piece(self):
        self.piece_id = self.canvas.create_image(self.grid_x * self.piece_size + self.piece_size / 2,
                                                 self.grid_y * self.piece_size + self.piece_size / 2,
                                                 image=self.image, anchor=tk.CENTER, tags="piece")
        self.canvas.tag_bind(self.piece_id, "<Button-1>", self.on_piece_click)

    def on_piece_click(self, event):
        self.canvas.lift(self.piece_id)
        self.canvas.bind("<B1-Motion>", self.on_piece_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_piece_release)

    def on_piece_drag(self, event):
        x, y = event.x, event.y
        self.canvas.coords(self.piece_id, x, y)

    def on_piece_release(self, event):
        x, y = event.x, event.y
        grid_x = min(max(int(x / self.piece_size), 0), (self.canvas.winfo_width() // self.piece_size) - 1)
        grid_y = min(max(int(y / self.piece_size), 0), (self.canvas.winfo_height() // self.piece_size) - 1)
        self.grid_x, self.grid_y = grid_x, grid_y
        self.update_position()
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def update_position(self):
        self.canvas.coords(self.piece_id, self.grid_x * self.piece_size + self.piece_size / 2,
                           self.grid_y * self.piece_size + self.piece_size / 2)

def main():
    root = tk.Tk()
    app = JigsawPuzzleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
