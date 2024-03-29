import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random

class JigsawPuzzleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Jigsaw Puzzle Game")

        self.canvas = tk.Canvas(master, width=800, height=600, bg="white")
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

        # Divide the image into puzzle pieces
        num_pieces_x = 4
        num_pieces_y = 3
        piece_width = self.original_image.width // num_pieces_x
        piece_height = self.original_image.height // num_pieces_y

        for y in range(num_pieces_y):
            for x in range(num_pieces_x):
                left = x * piece_width
                top = y * piece_height
                right = left + piece_width
                bottom = top + piece_height
                piece_image = self.original_image.crop((left, top, right, bottom))
                piece = PuzzlePiece(self.canvas, piece_image, x, y, piece_width, piece_height)
                self.pieces.append(piece)

    def shuffle_pieces(self):
        random.shuffle(self.pieces)
        for i, piece in enumerate(self.pieces):
            piece.grid_x = i % 4
            piece.grid_y = i // 4
            piece.update_position()

class PuzzlePiece:
    def __init__(self, canvas, image, grid_x, grid_y, width, height):
        self.canvas = canvas
        self.image = ImageTk.PhotoImage(image)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.width = width
        self.height = height
        self.piece_id = None

        self.create_piece()

    def create_piece(self):
        self.piece_id = self.canvas.create_image(self.grid_x * self.width + self.width / 2,
                                                 self.grid_y * self.height + self.height / 2,
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
        grid_x = min(max(int(x / self.width), 0), 3)
        grid_y = min(max(int(y / self.height), 0), 2)
        self.grid_x, self.grid_y = grid_x, grid_y
        self.update_position()
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def update_position(self):
        self.canvas.coords(self.piece_id, self.grid_x * self.width + self.width / 2,
                           self.grid_y * self.height + self.height / 2)

def main():
    root = tk.Tk()
    app = JigsawPuzzleGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
