from django.conf import settings

from .module_tree import ModuleTree

class PathResolver:
    class NoMatch(Exception):
        pass

    def __init__(self, root_module_name):
        self.root_module_name = root_module_name
        self.module_tree = ModuleTree(root_module_name)

    def call(self, path):
        try :
            return (self.get_handler_list(path), {})
        except self.NoMatch :
            pass

        if not settings.DEBUG :
            return

        try :
            return (self.get_handler_list(path), {})
        except self.NoMatch :
            pass

    def get_handler_list(self, path):
        previous_node = self.module_tree
        handler_list = [(previous_node.module, None)]

        while path :
            try :
                segment, rest = path.split('/', 1)
            except ValueError :
                segment = path
                rest = ''

            # Does the segment match a submodule name exactly?
            try :
                handler_node = previous_node.submodules[segment]
            except KeyError :
                pass
            else :
                handler_list.append((handler_node.module, None))
                path = rest
                previous_node = handler_node
                continue

            # Are there any "capturing" submodules defined?
            try :
                handler_node = previous_node.submodules['int__']
            except KeyError :
                pass
            else :
                try :
                    arg = int(segment)
                except ValueError :
                    pass
                else :
                    handler_list.append((handler_node.module, arg))
                    path = rest
                    previous_node = handler_node
                    continue

            try :
                handler_node = previous_node.submodules['string__']
            except KeyError :
                pass
            else :
                handler_list.append((handler_node.module, segment))
                path = rest
                previous_node = handler_node
                continue

            # If they have a path__ module defined, consume the entire remaining path
            try :
                handler_node = previous_node.submodules['path__']
            except KeyError :
                pass
            else :
                handler_list.append((handler_node.module, path))
                path = ''
                previous_node = handler_node
                continue

            raise self.NoMatch()

        return handler_list
