""""""


from typing import List


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
        self._should_exit = False

    def render(self):
        self._should_exit = False
        if self.__class__ == BaseRenderer:
            raise NotImplementedError('please define `render` in subclass')

    def move(self, direction):
        self.selected_option += direction

    def exit(self):
        self._should_exit = True

    def invoke_event(self, event='click', *args):
        return self.get_selected()._invoke(event, self, *args)

    def get_selected(self):
        return self.menu.options[self.selected_option]


class SimpleMenuRenderer(BaseRenderer):
    def get_number(self, value):
        if value == '':
            return self.selected_option
        try:
            value = int(value)
        except ValueError:
            print('Please enter a number.')
            return
        else:
            return value

    def render(self):
        super().render()
        if self.menu.label:
            label = self.menu.label + ':\t'
        else:
            label = ''
        label += '\t'.join(
            ':'.join((str(n), str(option.text)))
            for (n, option)
            in enumerate(self.menu.options)
            if option.text is not None)
        print(label)
        while not self._should_exit:
            value = input('Which option: ')
            value = self.get_number(value)
            if value is None:
                continue
            self.selected_option = value
            try:
                return self.get_selected()
            except IndexError:
                print('Invalid option: %s' % value)


class VerticalMenuRenderer(BaseRenderer):
    pass


BaseRenderer._render_classes['simple'] = SimpleMenuRenderer
BaseRenderer._render_classes['vertical'] = VerticalMenuRenderer


class Menu:
    options: List[MenuOption]

    def __init__(self,
                 label=None,
                 options: List[MenuOption] = None,
                 render_class='simple',
                 stay_open=True):
        if options is None:
            options = []
        self.label = label
        self.options = options
        self.render_class = render_class
        self.default_stay_open = stay_open

    @property
    def render_class(self):
        return self._render_class

    @render_class.setter
    def render_class(self, klass):
        self._render_class = BaseRenderer._render_classes.get(klass, klass)

    def render(self, renderer=None):
        self.stay_open = self.default_stay_open
        first_run = True
        while self.stay_open or first_run:
            first_run = False
            if renderer is None:
                renderer = self.render_class(self)
            action = renderer.render()
            if action is not None:
                result = action._invoke('click', renderer)
            else:
                result = None
        return result


del List


if __name__ == '__main__':
    options = [
        MenuOption('opt1', lambda menu: print(menu)),
        MenuOption('opt2', lambda menu: exec('raise Exception')),
        MenuOption(),
        MenuOption('abc', lambda menu: print('abc')),
        MenuOption('def', lambda menu: setattr(menu.menu, 'stay_open', False)),
    ]
    mymenu = Menu('Main Menu', options=options)
    mymenu.render()
