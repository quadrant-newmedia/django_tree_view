from django.conf import settings

from .view_tree import ViewTree

class PathResolver:
    class NoMatch(Exception):
        pass

    def __init__(self, root_module_name):
        self.root_module_name = root_module_name
        self.view_tree = ViewTree(root_module_name)

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
            self.view_tree = ViewTree(self.root_module_name)
            return (self.get_handler_list(path), {})
        except self.NoMatch :
            pass

    def get_handler_list(self, path):
        '''
            Returns a list of (view_tree_node, captured_argument) tuples.

            Will raise NoMatch if path cannot be mapped to a final view tree node (with module != None).

            Note: path should not have a leading '/'.
            If it does, we consider the path to start with an empty segment (which can still map to a string__ handler module).
        '''
        previous_node = self.view_tree
        handler_list = [(previous_node, None)]

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
                    node = previous_node.subtrees[segment]
                except KeyError :
                    pass
                else :
                    handler_list.append((node, None))
                    path = rest
                    previous_node = node
                    continue

                # Are there any "capturing" subtrees defined?
                try :
                    node = previous_node.subtrees['int__']
                except KeyError :
                    pass
                else :
                    try :
                        arg = int(segment)
                    except ValueError :
                        pass
                    else :
                        handler_list.append((node, arg))
                        path = rest
                        previous_node = node
                        continue

                try :
                    node = previous_node.subtrees['string__']
                except KeyError :
                    pass
                else :
                    handler_list.append((node, segment))
                    path = rest
                    previous_node = node
                    continue

            # If they have a path__ module defined, consume the entire remaining path
            try :
                node = previous_node.subtrees['path__']
            except KeyError :
                pass
            else :
                handler_list.append((node, path))
                path = ''
                previous_node = node
                continue

            raise self.NoMatch()

        if not handler_list[-1][0].module:
            raise self.NoMatch()

        return handler_list
