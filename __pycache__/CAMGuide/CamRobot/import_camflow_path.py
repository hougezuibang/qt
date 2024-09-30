import os, sys
PyRecipe_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PyRecipe_base_path = PyRecipe_path + r"\base"
PyRecipe_base_epcam_path = PyRecipe_path + r"\base\epcam"
if not PyRecipe_base_path in sys.path:
    sys.path.append(PyRecipe_base_path)
if not PyRecipe_base_epcam_path in sys.path:
    sys.path.append(PyRecipe_base_epcam_path)