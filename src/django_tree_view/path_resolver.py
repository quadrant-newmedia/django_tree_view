from django.conf import settings

from .module_tree import ModuleTree

class PathResolver:
    class NoMatch(Exception):
        pass

    def __init__(self, root_module_name):
        self.root_module_name = root_module_name
        self.module_tree = ModuleTree(root_module_name)

    def __call__(self, path):
        try :
            return (self.get_handler_list(path), {})
        except self.NoMatch :
            pass

        if not settings.DEBUG :
            return

        try :
            '''
                Reload the entire module tree, in case a new module has been added
                (django's runserver won't auto-reload when adding new modules, since you don't have to update existing files to import them)

                Note - this does not catch:
                    - modules that were deleted (cached, same response is returned)
                    - directory already existed, you received 404, then you added __init__.py
            '''
            self.module_tree = ModuleTree(self.root_module_name)
            return (self.get_handler_list(path), {})
        except self.NoMatch :
            pass

    def get_handler_list(self, path):
        '''
            Note: path should not have a leading '/'.
            If it does, we consider the path to start with an empty segment (which can still map to a string__ handler module).
        '''
        previous_node = self.module_tree
        handler_list = [(previous_node.module, None)]

        while path :
            '''
                Notice - the path must end in 
            '''

            '''
                Note: the path must end with / for the last segment to match a "segment handler" (ie. fixed, int__, or str__).
                If the path does not end with a /, the last segment can only match a path__ handler.

                This is by design. We don't want multiple urls (ie. with and without trailing /) to map to the same handler. Trailing / are basically necessary in urls for relative links to work.

                TODO - if url is missing trailing '/', but would have matched otherwise, should we redirect? Provide this as an option? That's how Django works.
            '''
            try :
                segment, rest = path.split('/', 1)
            except ValueError :
                pass
            else:
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
