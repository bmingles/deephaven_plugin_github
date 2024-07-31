rm -rf build dist

# Build js
pushd src/js
npm run build
popd

# Build python
python -m build --wheel
pip install --upgrade --no-deps --force-reinstall dist/deephaven_plugin_github-0.0.1.dev0-py3-none-any.whl
