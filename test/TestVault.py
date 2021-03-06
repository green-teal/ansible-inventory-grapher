import os
import unittest

import ansibleinventorygrapher.inventory


class TestVault(unittest.TestCase):

    def test_vault_password_file(self):
        invfile = os.path.join('test', 'vault', 'inventory')
        vault_password_files = [os.path.join('test', 'vault', 'vaultpass')]
        inventory_mgr = ansibleinventorygrapher.inventory.InventoryManager(invfile, False, vault_password_files)
        hostname = "web-01"
        host = inventory_mgr.inventory.get_host(hostname)
        group = inventory_mgr.inventory.get_group("web")
        the_vars = ansibleinventorygrapher.tidy_all_the_variables(host, inventory_mgr)
        self.assertEqual(the_vars[group]["text"], "hello")

    def test_vault_password_file(self):
        invfile = os.path.join('test', 'vault', 'inventory')
        vault_password_files = [os.path.join('test', 'vault', 'vaultpass'),
                                os.path.join('test', 'vault', 'notthevaultpass')]
        inventory_mgr = ansibleinventorygrapher.inventory.InventoryManager(invfile, False, vault_password_files)
        hostname = "web-01"
        host = inventory_mgr.inventory.get_host(hostname)
        group = inventory_mgr.inventory.get_group("web")
        the_vars = ansibleinventorygrapher.tidy_all_the_variables(host, inventory_mgr)
        self.assertEqual(the_vars[group]["text"], "hello")

    def test_vault_ids(self):
        invfile = os.path.join('test', 'vault_ids', 'inventory')
        vault_ids = ['another_vault@' + os.path.join('test', 'vault_ids', 'vaultpass')]
        inventory_mgr = ansibleinventorygrapher.inventory.InventoryManager(invfile, False, [], vault_ids)
        hostname = "web-01"
        host = inventory_mgr.inventory.get_host(hostname)
        the_vars = ansibleinventorygrapher.tidy_all_the_variables(host, inventory_mgr)
        self.assertEqual(the_vars[host]["hello"], "world")

    def test_no_vault_pass(self):
        invfile = os.path.join('test', 'vault', 'inventory')
        try:
            inventory_mgr = ansibleinventorygrapher.inventory.InventoryManager(invfile, False, [])
            hostname = "web-01"
            host = inventory_mgr.inventory.get_host(hostname)
            the_vars = ansibleinventorygrapher.tidy_all_the_variables(host, inventory_mgr)
            raise RuntimeError
        except ansibleinventorygrapher.inventory.NoVaultSecretFound:
            pass  # expected behaviour

    def test_inline_vault_without_password(self):
        invfile = os.path.join('test', 'vault', 'inventory')
        inventory_mgr = ansibleinventorygrapher.inventory.InventoryManager(invfile, False, [])
        hostname = "inline-01"
        host = inventory_mgr.inventory.get_host(hostname)
        group = inventory_mgr.inventory.get_group("inline")
        the_vars = ansibleinventorygrapher.tidy_all_the_variables(host, inventory_mgr)
        self.assertTrue('text' in the_vars[group])
        self.assertFalse('text' in the_vars[host])
