# ===============================
# PATCH LOADER SYSTEM
# ===============================
# Automatically loads and applies patches with hooks

import os
import sys
import importlib.util
import inspect
from typing import Dict, List, Callable, Any

class PatchSystem:
    def __init__(self, patches_dir: str = "patches"):
        self.patches_dir = patches_dir
        self.loaded_patches = {}
        self.hooks = {
            'init': [],
            'before_run': [],
            'after_run': [],
            'on_error': [],
            'on_success': [],
            'cleanup': []
        }
        
    def load_patches(self):
        """Load all patch files from the patches directory."""
        if not os.path.exists(self.patches_dir):
            os.makedirs(self.patches_dir)
            print(f"[i] Created patches directory: {self.patches_dir}")
            return
            
        patch_files = [f for f in os.listdir(self.patches_dir) 
                      if f.startswith('patch_') and f.endswith('.py')]
        
        for patch_file in patch_files:
            patch_name = patch_file[:-3]  # Remove .py extension
            patch_path = os.path.join(self.patches_dir, patch_file)
            
            try:
                spec = importlib.util.spec_from_file_location(patch_name, patch_path)
                patch_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(patch_module)
                
                self.loaded_patches[patch_name] = patch_module
                self._register_hooks(patch_module, patch_name)
                print(f"[i] Loaded patch: {patch_name}")
                
            except Exception as e:
                print(f"[!] Failed to load patch {patch_file}: {e}")
                
    def _register_hooks(self, patch_module, patch_name):
        """Register hook functions from a patch module."""
        for name, func in inspect.getmembers(patch_module, inspect.isfunction):
            if name.startswith('hook_'):
                hook_type = name.split('_', 1)[1]  # Extract hook type
                if hook_type in self.hooks:
                    self.hooks[hook_type].append((patch_name, func))
                    
    def execute_hooks(self, hook_type: str, *args, **kwargs):
        """Execute all hooks of a given type."""
        results = []
        for patch_name, hook_func in self.hooks.get(hook_type, []):
            try:
                result = hook_func(*args, **kwargs)
                results.append((patch_name, result))
            except Exception as e:
                print(f"[!] Hook {hook_type} failed in {patch_name}: {e}")
        return results
        
    def get_patch_function(self, patch_name: str, function_name: str):
        """Get a specific function from a loaded patch."""
        if patch_name in self.loaded_patches:
            return getattr(self.loaded_patches[patch_name], function_name, None)
        return None

# Global patch system instance
patch_system = PatchSystem()

if __name__ == "__main__":
    patch_system.load_patches()
    print(f"[i] Loaded {len(patch_system.loaded_patches)} patches")
    print(f"[i] Registered hooks: {[(k, len(v)) for k, v in patch_system.hooks.items() if v]}")
