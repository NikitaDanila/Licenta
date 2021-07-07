import time
import threading
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from threading import get_ident
    except ImportError:
        from _thread import get_ident


class CameraEvent(object):
    """Clasa aceasta porneste un event cand avem un nou frame disponibil"""
    def __init__(self):
        self.events = {}

    def wait(self):
        """fircare client are cate un thread si trebuie sa astepte un nou frame"""
        ident = get_ident()
        if ident not in self.events:
            # acesta este un nou client
            # adaugam clientul la self.events
            # fiecare intrare are doua elemente, threading.Event() si un timp
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """Iaceasta functie este apelata automat cand avem un nou frame."""
        now = time.time()
        remove = None
        for ident, event in self.events.items():
            if not event[0].isSet():
                # daca evenimentul clientului nu este setat, il setam acum
                # actualizam timpul de pornire a evenimentului acum
                event[0].set()
                event[1] = now
            else:
                # daca evenimetul unui client este setat inseamna ca nu a 
                # procesat vechiul frame si daca acesta nu este actualizat
                # in 5 secunde presupunem ca a plecat si stergem evenimentul
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """apelat de la fiecare thread al clientului cand un frame este procesat"""
        self.events[get_ident()][0].clear()


class BaseCamera(object):
    thread = None  # thread care citeste frame-uri din camera
    frame = None  # frame-ul curent este salvat aici
    last_access = 0  # ultimul timp cand a accesat un client camera
    event = CameraEvent()

    def __init__(self):
        """Pornin thread-ul camerei, daca nu este deja pornit."""
        if BaseCamera.thread is None:
            BaseCamera.last_access = time.time()

            # Pornin thread-ul camerei
            BaseCamera.thread = threading.Thread(target=self._thread)
            BaseCamera.thread.start()

            # Asteptam pana avem frame-uri disponibile
            while self.get_frame() is None:
                time.sleep(0)

    def get_frame(self):
        """Returnam frame-ul curent."""
        BaseCamera.last_access = time.time()

        # asteptam un event al thread-ului
        BaseCamera.event.wait()
        BaseCamera.event.clear()

        return BaseCamera.frame

    @staticmethod
    def frames():
        raise RuntimeError('Must be implemented by subclasses.')

    @classmethod
    def _thread(cls):
        """Generator de thread-uri."""
        print('Starting camera thread.')
        frames_iterator = cls.frames()
        for frame in frames_iterator:
            BaseCamera.frame = frame
            BaseCamera.event.set()  # trimitem semanle clientilor
            time.sleep(0)

            # daca nu am avut clienti in ultimile 10 sec 
            # atunci oprim thread-ul
            if time.time() - BaseCamera.last_access > 10:
                frames_iterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None