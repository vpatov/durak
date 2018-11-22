import colorama


def placestr(place):
    if place == 1:
        return '1st'
    elif place == 2:
        return '2nd'
    elif place == 3:
        return '3rd'
    else:
        return str(place) + 'th'

def cstr(string,color='RED'):
    return getattr(colorama.Fore,color.upper()) + string + colorama.Fore.RESET

def debug_func(func):
    def echo_func(*func_args, **func_kwargs):
        if func_kwargs:
            print('{}({},{})'.format(cstr(func.__name__,"YELLOW"),func_args,func_kwargs))
        else:
            print('{}({})'.format(cstr(func.__name__,"YELLOW"),func_args))

        return func(*func_args, **func_kwargs)
    return echo_func

def decorate_class_functions(decorator):
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)) and not attr.startswith('__'):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate

