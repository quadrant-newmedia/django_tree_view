from datetime import date
import os
from django.test import TestCase, override_settings

from django.urls import resolve, reverse
from django.urls.exceptions import Resolver404

from django_tree_view import make_tree_view
from django_tree_view.view_tree import ViewTree, ConfigurationError
from django_tree_view.path_resolver import PathResolver

class ViewTreeTestCase(TestCase):
    def test_missing_init_message(self):
        self.assertRaisesMessage(
            ConfigurationError,
            'The root of a module tree must be a python package containing an __init__.py file',
            ViewTree,
            'tests.view_tree_with_no_init'
        )

    def test_module_tree_returns_correct_structur(self):
        t = ViewTree('tests.module_tree_structure_test')
        self.assertEqual(set(list(t.subtrees.keys())), set(['a', 'a2']))
        d = t.subtrees['a'].subtrees['b'].subtrees['c'].subtrees['d']
        self.assertEqual(0, len(d.subtrees))

    def test_raises_import_error(self):
        try :
            ViewTree('tests.view_tree_with_import_error')
        except ImportError as e :
            self.assertEqual(e.name, 'fake_module')

@override_settings(ROOT_URLCONF='tests.urls')
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

    def test_no_terminal_view_tree_node_does_not_resolve(self):
        with self.assertRaises(Resolver404) :
            resolve('/no_view_tree_node/')
        # Now verify that a sub-url with view_tree_node.py DOES resolve:
        resolve('/no_view_tree_node/sub_node/')


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

    def test_date_is_captured(self):
        r = resolve('/dates/2020-02-01/')
        handlers = r.args
        self.assertEqual(handlers[0][1], None)
        self.assertEqual(handlers[1][1], None)
        self.assertEqual(handlers[2][1], date(2020, 2, 1))
    def test_non_date_does_not_resolve(self):
        with self.assertRaises(Resolver404) :
            resolve('/dates/2020-02-444/')

    def test_string_captured_before_path(self):
        r = resolve('/multi_capture/banana/')
        handlers = r.args
        self.assertEqual(handlers[-1][1], 'banana')

    def test_path_is_captured(self):
        r = resolve('/path_capture/banana/pancake')
        handlers = r.args
        self.assertEqual(handlers[-1][1], 'banana/pancake')

@override_settings(ROOT_URLCONF='tests.urls')
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

# TODO - test django_page_visibility support