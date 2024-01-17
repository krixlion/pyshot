import keyboard
import tkinter as tk
import win32clipboard as clip
from io import BytesIO
from PIL import Image, ImageTk, ImageGrab

def save_image_to_clipboard(img: Image):
    # Convert image to format compatible with win32 API.
    buffer = BytesIO()
    img.convert('RGB').save(buffer, 'BMP')
    data = buffer.getvalue()[14:]
    buffer.close()

    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(clip.CF_DIB, data) # Save as a bitmap.
    clip.CloseClipboard()


class MouseTracker():
    """
    Tkinter Canvas mouse position widget.
    It's responsible for tracking cursor coordinates and displaying cross-hair lines.
    """

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        width = self.canvas.cget('width')
        height = self.canvas.cget('height')

        # Create canvas cross-hair lines.
        xhair_opts = dict(dash=(3, 2), fill='white', state=tk.HIDDEN)
        self.lineIds = (self.canvas.create_line(0, 0, 0, height, **xhair_opts), self.canvas.create_line(0, 0, width,  0, **xhair_opts))

    def register(self, updateHandler=lambda start, end: None, quitHandler=lambda: None):
        """ Registers canvas handlers listening for mouse events. """
        
        self.updateHandler = updateHandler
        self.quitHandler = quitHandler
        self.canvas.bind("<Button-1>", self.saveStartCoords) # When LMB is pressed and held.
        self.canvas.bind("<B1-Motion>", self.updateXHair) # When cursor is moved while holding LMB.
        self.canvas.bind("<ButtonRelease-1>", self.quit) # When LMB is released.
    
    def saveStartCoords(self, event: tk.Event):
        """ Saves coords of the point where LMB was pressed. """
        
        self.start = (event.x, event.y)  

    def updateXHair(self, event: tk.Event):
        """ Renders cross-hair lines and invokes previously saved handler. """

        self.canvas.coords(self.lineIds[0], event.x, 0, event.x, self.canvas.cget('height'))
        self.canvas.coords(self.lineIds[1], 0, event.y, self.canvas.cget('width'), event.y)
        
        # Display cross-hairs.
        for lineId in self.lineIds:
            self.canvas.itemconfigure(lineId, state=tk.NORMAL)
            
        self.updateHandler(self.start, (event.x, event.y))  # User callback.

    def quit(self, event: tk.Event): # Must match this signature.
        """ Hides cross-hair lines and invokes previously saved handler. """
        
        # Hide cross-hairs.
        for lineId in self.lineIds:
            self.canvas.itemconfigure(lineId, state=tk.HIDDEN)

        self.quitHandler()


class Selection:
    """ 
    Widget to display a rectangular selection area on given canvas
    defined by two points representing its diagonal.
    """
    
    def __init__(self, canvas: tk.Canvas, outer_opts):
        self.canvas = canvas
        width = self.canvas.cget('width')
        height = self.canvas.cget('height')
        
        # Separate options for area inside rectanglar selection.
        inner_opts = dict(dash=(2, 2), fill='', outline='white', state=tk.HIDDEN)
        
        self.rects = (
            # Area outside selection.
            self.canvas.create_rectangle(0, 0,  width, 0, **outer_opts), # Bottom.
            self.canvas.create_rectangle(0, 0,  0, 1, **outer_opts), # Side.
            self.canvas.create_rectangle(1, 0,  width, 1, **outer_opts), # Opposite side.
            self.canvas.create_rectangle(0, 1,  width, height, **outer_opts), # Top.
            
            # Selection area.
            self.canvas.create_rectangle(0, 0,  1, 1, **inner_opts)
        )

    def updateCoords(self, d1, d2):
        """ Updates selection area coordinates. """

        width = self.canvas.cget('width')
        height = self.canvas.cget('height')

        # Update coords of all rectangles.
        self.canvas.coords(self.rects[0], 0, 0,  width, d1[1]), # Bottom.
        self.canvas.coords(self.rects[1], 0, d1[1],  d1[0], d2[1]), # Side.
        self.canvas.coords(self.rects[2], d2[0], d1[1],  width, d2[1]), # Opposite side.
        self.canvas.coords(self.rects[3], 0, d2[1],  width, height), # Top.

        self.canvas.coords(self.rects[4], d1[0], d1[1],  d2[0], d2[1]), # Selection rectangle.

        # Make sure all areas are visible.
        for rect in self.rects:  
            self.canvas.itemconfigure(rect, state=tk.NORMAL)

    def getImage(self):
        """ Returns an image of selected area. """
        
        coords = self.canvas.coords(self.rects[4])
        return ImageGrab.grab(bbox=coords)


class ImageCropper():
    
    def __init__(self, title: str, bgColor: str, img: Image):
        
        # Init main window.
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry('%sx%s' % (img.width, img.height))
        self.window.configure(background=bgColor)
        self.window.attributes('-topmost', True) # Make the window appear on top.
        self.window.attributes('-fullscreen', True)

        # Convert the image to a Tkinter-compatible format.
        photo_img = ImageTk.PhotoImage(img)

        self.canvas = tk.Canvas(self.window, width=photo_img.width(), height=photo_img.height(), cursor='tcross', highlightbackground='red', highlightthickness=1, borderwidth=0)
        self.canvas.pack(expand=True)

        self.canvas.create_image(0, 0, image=photo_img, anchor=tk.NW)
        self.canvas.img = photo_img  # Set window background.

        # Default selection style options.
        select_opts = dict(dash=(2, 2), stipple='gray25', fill='black', outline='')
        
        self.selection = Selection(self.canvas, select_opts)

        MouseTracker(self.canvas).register(self.selection.updateCoords, self.quit)

    def quit(self):
        """ Saves the selected area to clipboard and closes the window. """
        
        save_image_to_clipboard(self.selection.getImage())
        self.window.destroy()
    
    def run(self):
        """ 
        Renders the main window and starts up it's event loop.
        Blocks until the window is closed.
        """
        
        self.window.mainloop()


if __name__ == '__main__':
    keyboard.add_hotkey('win+ctrl+shift+s', lambda : ImageCropper('PyShot', 'red', ImageGrab.grab()).run())
    keyboard.wait('ctrl+c')
