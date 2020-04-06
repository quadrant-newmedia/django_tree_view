import os
from django.test import TestCase, override_settings

from django.urls import resolve, reverse
from django.urls.exceptions import Resolver404

from django_tree_view import make_tree_view, NotATreeViewPath, is_get_allowed
from django_tree_view.module_tree import ModuleTree, ConfigurationError
from django_tree_view.path_resolver import PathResolver

class ModuleTreeTestCase(TestCase):
    def test_missing_init_message(self):
        self.assertRaisesMessage(
            ConfigurationError,
            'The root of a module tree must be a python package containing an __init__.py file',
            ModuleTree,
            'django_tree_view.tests.view_tree_with_no_init'
        )

    def test_module_tree_returns_correct_structur(self):
        t = ModuleTree('django_tree_view.tests.module_tree_structure_test')
        self.assertEqual(set(list(t.submodules.keys())), set(['a', 'a2']))
        d = t.submodules['a'].submodules['b'].submodules['c'].submodules['d']
        self.assertEqual(0, len(d.submodules))

@override_settings(ROOT_URLCONF='django_tree_view.tests.urls')
class PathResolverTestCase(TestCase):
    def test_does_not_resolve(self):
        with self.assertRaises(Resolver404) :
            resolve('/does_not_exist')

    def test_resolves(self):
        try :
            resolve('/foo/')
        except Resolver404 :
            self.fail('valid tree view path did not resolve')

    def test_deep_does_not_resolve(self):
        with self.assertRaises(Resolver404) :
            resolve('/foo/does_not_exist/')

    def test_missing_trailing_slash_does_not_resolve(self):
        with self.assertRaises(Resolver404) :
            resolve('/foo')

    def test_int_is_captured(self):
        r = resolve('/books/1/')
        handlers = r.args
        self.assertEqual(handlers[0][1], None)
        self.assertEqual(handlers[1][1], None)
        self.assertEqual(handlers[2][1], 1)

    def test_non_int_is_not_captured(self):
        with self.assertRaises(Resolver404) :
            resolve('/books/1a/')

    def test_int_captured_before_string(self):
        r = resolve('/multi_capture/1/')
        handlers = r.args
        self.assertEqual(handlers[-1][1], 1)

    def test_string_captured_before_path(self):
        r = resolve('/multi_capture/banana/')
        handlers = r.args
        self.assertEqual(handlers[-1][1], 'banana')

    def test_path_is_captured(self):
        r = resolve('/path_capture/banana/pancake')
        handlers = r.args
        self.assertEqual(handlers[-1][1], 'banana/pancake')

@override_settings(ROOT_URLCONF='django_tree_view.tests.urls')
# Add view tree to template dirs:
@override_settings(TEMPLATES=[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'view_tree')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
])
class IntegrationTestCase(TestCase):
    def test_not_found(self):
        r = self.client.get('/bar/')
        self.assertEqual(r.status_code, 404)

    def test_method_not_allowed(self):
        r = self.client.get('/books/')
        self.assertEqual(r.status_code, 405)

    def test_options(self):
        r = self.client.options('/books/')
        self.assertEqual(r['allow'], 'options')

    def test_options_with_multiple_methods(self):
        r = self.client.options('/books/67/')
        self.assertEqual(r['allow'], 'get, post, options')

    def test_preprocess_functions_called_and_data_passed_along(self):
        r = self.client.get('/books/67/')
        self.assertEqual(r.content, b'root:1:book_id:67')

    def test_post_fails_csrf(self):
        r = self.client.post('/books/67/')
        self.assertEqual(r.status_code, 403)

    def test_post_with_csrf_exempt_works(self):
        r = self.client.post('/csrf_exempt/')
        self.assertEqual(r.status_code, 200)

    def test_relative_template_works(self):
        r = self.client.get('/with_template/')
        self.assertEqual(r.content, b'basic template')
    def test_named_relative_template_in_subfolder_works(self):
        r = self.client.get('/with_named_template/')
        self.assertEqual(r.content, b'template a')

@override_settings(ROOT_URLCONF='django_tree_view.tests.urls')
class IsGetAllowedTestCase(TestCase):
    def test_template_view_raises_not_a_tree_view(self):
        with self.assertRaises(NotATreeViewPath):
            is_get_allowed('/template_view', None)
    def test_nonexistent_url_raises_not_a_tree_view(self):
        with self.assertRaises(NotATreeViewPath):
            is_get_allowed('/fake', None)
    def test_allowed_path_returns_true(self):
        self.assertTrue(is_get_allowed('/books/', None))
    def test_non_allowed_path_returns_false(self):
        self.assertFalse(is_get_allowed('/books/5/raise_early_return/', None))
    # TODO - tests with actual user?