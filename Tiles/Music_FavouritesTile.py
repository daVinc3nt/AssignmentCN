import ntpath
import Paths

from io import BytesIO
from PyQt5 import QtWidgets, QtGui, QtCore
from .Tile import Tile


class MusicTile(Tile):  # Music Tile
    playing = QtCore.pyqtSignal(object)  # path
    addFavourite = QtCore.pyqtSignal(object)
    addToCollection = QtCore.pyqtSignal(object, bool)

    def __init__(self, file_path="", *args, **kwargs):
        super(MusicTile, self).__init__(*args, **kwargs)

        self.file_path = file_path

        if title and title.isspace():
            title = ""

        if not title:
            title = ntpath.basename(file_path)


        self.setLayout(QtWidgets.QVBoxLayout())

        self.setObjectName("MusicTile")

        self.thumb_nail = QtWidgets.QLabel()
        self.thumb_nail.setScaledContents(True)
        self.thumb_nail.setLayout(QtWidgets.QVBoxLayout())

        self.music_title = QtWidgets.QLabel(text=title)
        self.music_title.setMaximumHeight(30)
        self.setToolTip(title)

        self.btns = QtWidgets.QWidget(objectName="ButtonGroup")
        self.btns.setLayout(QtWidgets.QHBoxLayout())

        btn_grp = QtWidgets.QButtonGroup(self)

        self._playing = False
        self._favourite = False
        self._collection = False

        self.play_btn = QtWidgets.QPushButton(objectName="PlayButton")
        self.play_btn.setToolTip("Play")
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))
        self.play_btn.setFixedSize(50, 50)

        self.favourite = QtWidgets.QPushButton(objectName="Favourite")
        self.favourite.setToolTip("Mark Favourite")
        self.favourite.setIcon(QtGui.QIcon(Paths.STAR_UNFILLED))
        self.favourite.setFixedSize(50, 50)

        self.collection = QtWidgets.QPushButton(objectName="Collection")
        self.collection.setToolTip("Add to Collection")
        self.collection.setIcon(QtGui.QIcon(Paths.COLLECTION))
        self.collection.setFixedSize(50, 50)

        btn_grp.addButton(self.play_btn)
        btn_grp.addButton(self.favourite)
        btn_grp.addButton(self.collection)
        btn_grp.buttonClicked.connect(self.clicked)

        self.btns.layout().addWidget(self.collection, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.favourite, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.play_btn, alignment=QtCore.Qt.AlignBottom)

        self.btns.hide()

        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(5)
        self.shadow_effect.setOffset(3, 3)
        self.shadow_effect.setColor(QtGui.QColor(255, 255, 255))

        self.play_btn.setGraphicsEffect(self.shadow_effect)
        self.favourite.setGraphicsEffect(self.shadow_effect)
        self.collection.setGraphicsEffect(self.shadow_effect)

        self.btns.setGraphicsEffect(self.shadow_effect)

        self.thumb_nail.layout().addWidget(self.btns, alignment=QtCore.Qt.AlignBottom)
        self.layout().addWidget(self.thumb_nail)
        self.layout().addWidget(self.music_title)

        self._children = set()
        self._collection_name = None

    def addChild(self, child):
        self._children.add(child)

    def getFile(self):
        return self.file_path

    def getThumbnail(self):
        return self.thumb_nail.pixmap()

    def getTitle(self):
        return self.music_title.text()

    def getCollectionName(self):
        return self._collection_name

    def setCollectionName(self, name):
        self._collection_name = name

    def properties(self):
        return [self._playing, self._favourite, self._collection]

    def removeChild(self, child):
        try:
            self._children.remove(child)
        except KeyError:
            pass

    def getChildren(self):
        return self._children

    def isPlaying(self):
        return self._playing

    def update_children(self):
        copied = self._children.copy()
        for item in copied:
            try:
                if self.isPlaying():
                    item.update_play()

                else:
                    item.update_pause()

                try:
                    item.checkFavourite()

                except (NameError, AttributeError):
                    raise NotImplementedError("'Check Favourite' must be implemented")

            except RuntimeError as e:
                print(e)

    def updateCollection(self):
        self._collection = not self._collection

        if self._collection:
            self.collection.setIcon(QtGui.QIcon(Paths.COLLECTION_GRAY))

        else:
            self.collection.setIcon(QtGui.QIcon(Paths.COLLECTION))
            self._collection_name = None

    def clicked(self, btn: QtWidgets.QPushButton = None):
        obj_name = btn.objectName()

        if obj_name == "PlayButton":
            self._playing = not self._playing

            if self._playing:
                self.play()

            else:
                self.pause()

            self.playing.emit(self)
            self.update_children()

        elif obj_name == "Favourite":
            self._favourite = not self._favourite

            self.addFavourite.emit(self)

            if self._favourite:
                self.favourite.setIcon(QtGui.QIcon(Paths.STAR_FILLED))

            else:
                self.favourite.setIcon(QtGui.QIcon(Paths.STAR_UNFILLED))

            self.update_children()

        elif obj_name == "Collection":

            self._collection = not self._collection
            self.addToCollection.emit(self, self._collection)

            if self._collection:
                self.collection.setIcon(QtGui.QIcon(Paths.COLLECTION_GRAY))
                self.collection.setToolTip("Remove from collection")

            else:
                self.collection.setIcon(QtGui.QIcon(Paths.COLLECTION))
                self.collection.setToolTip("Add to collection")
                self._collection_name = None


class FavouritesTile(Tile):  # Favourites tile.

    def __init__(self, parent: MusicTile, *args, **kwargs):
        super(FavouritesTile, self).__init__(*args, **kwargs)

        self.setObjectName("Favourite")
        self.setLayout(QtWidgets.QVBoxLayout())
        self.parent = parent
        self.parent.addChild(self)

        self.thumb_nail = QtWidgets.QLabel()
        self.thumb_nail.setScaledContents(True)
        self.thumb_nail.setPixmap(self.parent.getThumbnail())
        self.thumb_nail.setLayout(QtWidgets.QVBoxLayout())

        self.title = QtWidgets.QLabel(self.parent.getTitle())
        self.title.setMaximumHeight(30)

        btns = QtWidgets.QButtonGroup(self)

        self.play_btn = QtWidgets.QPushButton(objectName="PlayButton")
        self.play_btn.setFixedSize(50, 50)
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

        self.favourite = QtWidgets.QPushButton(objectName="Favourite")
        self.favourite.setToolTip("remove from favourite")
        self.favourite.setFixedSize(50, 50)
        self.favourite.setIcon(QtGui.QIcon(Paths.STAR_FILLED))

        if self.parent.isPlaying():
            self.update_play()

        btns.addButton(self.play_btn)
        btns.addButton(self.favourite)
        btns.buttonClicked.connect(self.clicked)

        self.btns = QtWidgets.QWidget(objectName="ButtonGroup")
        self.btns.setLayout(QtWidgets.QHBoxLayout())
        self.btns.hide()

        self.btns.layout().addWidget(self.favourite, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.play_btn, alignment=QtCore.Qt.AlignBottom)

        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(5)
        self.shadow_effect.setOffset(3, 3)
        self.shadow_effect.setColor(QtGui.QColor(255, 255, 255))

        self.play_btn.setGraphicsEffect(self.shadow_effect)
        self.favourite.setGraphicsEffect(self.shadow_effect)
        self.btns.setGraphicsEffect(self.shadow_effect)

        self.thumb_nail.layout().addWidget(self.btns, alignment=QtCore.Qt.AlignBottom)
        self.layout().addWidget(self.thumb_nail)
        self.layout().addWidget(self.title)

    def update_play(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PAUSE))

    def update_pause(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

    def pause(self):
        self.update_pause()
        self.play_btn.setToolTip("Play")
        self.parent.clicked(self.play_btn)

    def play(self):
        self.update_play()
        self.play_btn.setToolTip("Pause")
        self.parent.clicked(self.play_btn)

    def clicked(self, btn):

        if btn == self.play_btn:
            if self.parent.isPlaying():
                self.pause()

            else:
                self.play()

        elif btn == self.favourite:
            self.parent.clicked(btn)

    def deleteLater(self) -> None:
        self.parent.removeChild(self)
        super(FavouritesTile, self).deleteLater()

    def checkFavourite(self):  # do not remove this
        pass
