import { type WidgetPlugin, PluginType } from '@deephaven/plugin';
import { vsGraph } from '@deephaven/icons';
import { DeephavenPluginGithubView } from './DeephavenPluginGithubView';

// Register the plugin with Deephaven
export const DeephavenPluginGithubPlugin: WidgetPlugin = {
  // The name of the plugin
  name: 'deephaven-plugin-github',
  // The type of plugin - this will generally be WIDGET_PLUGIN
  type: PluginType.WIDGET_PLUGIN,
  // The supported types for the plugin. This should match the value returned by `name`
  // in DeephavenPluginGithubType in deephaven_plugin_github_type.py
  supportedTypes: 'DeephavenPluginGithub',
  // The component to render for the plugin
  component: DeephavenPluginGithubView,
  // The icon to display for the plugin
  icon: vsGraph,
};

export default DeephavenPluginGithubPlugin;
