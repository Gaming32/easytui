""""""


class MenuOption:
    def __init__(self, text=None, action=None):
        self.text = text
        self._handlers = self._default_handlers.copy()
        self.register('click', action)
        if text is None:
            self.register('hover', self._skip_option)

    def register(self, event='click', action=None):
        if action is None:
            action = self._default_handlers[event]
        self._handlers[event] = action

    def _skip_option(self, menu, direction):
        menu.move(direction)
        self._invoke('click', menu)

    def _invoke(self, event, menu, *args):
        return self._handlers[event](menu, *args)

    _default_handlers = {
        'click': (lambda menu: None),
        'hover': (lambda menu: None),
    }


class BaseRenderer:
    _render_classes = {}

    def __init__(self, menu):
        self.menu = menu
        self.selected_option = 0

    def render(self):
        pass

    def move(self):
        pass


class VerticalMenuRenderer(BaseRenderer):
    pass


BaseRenderer._render_classes['vertical'] = VerticalMenuRenderer


class Menu:
    def __init__(self, options, render_class='vertical'):
        self.render_class = render_class

    @property
    def render_class(self):
        return self._render_class

    @render_class.setter
    def render_class(self, klass):
        self._render_class = BaseRenderer._render_classes.get(klass, klass)

    def render(self, renderer=None):
        if renderer is None:
            renderer = self.render_class(self)
        renderer.render()
        return renderer
