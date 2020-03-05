from django.test import TestCase, override_settings

from django_tree_view.module_tree import ModuleTree, ConfigurationError
from django_tree_view.path_resolver import PathResolver

# Sample - you can override any settings you require for your tests
# @override_settings(ROOT_URLCONF='django_tree_view.tests.urls')
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
class IntegrationTestCase(TestCase):
    def test_not_found(self):
        r = self.client.get('/bar/')
        self.assertEqual(r.status_code, 404)





    # Samples:
    # def test_normal_path_before_dynamic_returns_correct_response(self):
    #     r = self.client.get('/path_before/')
    #     self.assertEqual(r.content, b'path before')
    # def test_normal_path_after_dynamic_returns_correct_response(self):
    #     r = self.client.get('/path_after/')
    #     self.assertEqual(r.content, b'path after')

    # def test_dynamic_path_returns_expected_response(self):
    #     r = self.client.get('/bar/')
    #     self.assertEqual(r.content, b'bar from dynamic')

    # def test_dynamic_path_func_receives_correct_args(self):
    #     r = self.client.get('/baz/')
    #     self.assertEqual(r.status_code, 200)

    # def test_included_dynamic_path_func_receives_correct_args(self):
    #     r = self.client.get('/included/baz/')
    #     self.assertEqual(r.status_code, 200)

    # def test_path_before_can_be_reversed(self):
    #     self.assertEqual(reverse('path_before_name'), '/path_before/')
    # def test_path_after_with_params_can_be_reversed(self):
    #     self.assertEqual(reverse('path_after_name', kwargs=dict(value='BAZ')), '/path_after/BAZ/')
