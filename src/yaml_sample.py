"""YAML Parsing Sample."""
import logging

import click
import yaml

_LOG_LEVEL_MAP = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
    'FATAL': logging.FATAL
}


def traverse_yaml_value(node):
    """Traverse Yaml value."""
    if not isinstance(node, dict):
        logging.info(node)
        return [node]
    ret = [] 
    for node_value in node.values():
        ret += traverse_yaml_value(node_value)
    return ret


def traverse_yaml_key_dfs(node):
    """Traverse Yaml Key."""
    ret = []
    for key, value in node.items():
        if not isinstance(value, dict):
            logging.info(key)
            ret.append(key)
        else:
            logging.info(key)
            ret.append(key)
            ret += traverse_yaml_key_dfs(value)
    return ret


def traverse_yaml_key_bfs(node):
    """Traverse Yaml Key."""
    ret = []
    for key, value in node.items():
        if not isinstance(value, dict):
            logging.info(key)
            ret.append(key)
        else:
            ret += traverse_yaml_key_bfs(value)
    return ret


def compare_yaml(from_node, to_node):
    """Compare Node."""
    for key, value in from_node.items():
        if key not in to_node:
            return False
        if not isinstance(value, dict):
            if value != to_node[key]:
                return False
            return True
        if compare_yaml(from_node=value, to_node=to_node[key]) is False:
            return False
    return True


@click.command()
@click.option('--log-level', '-ll',
              type=click.Choice(list(_LOG_LEVEL_MAP.keys()),
                                case_sensitive=True),
              required=False, default='INFO', help='Specify logging level')
@click.option('--yaml-file', '-y', required=True,
              type=click.File(mode='r', encoding='utf-8-sig'))
@click.option('--other-yaml-file', '-o', required=False,
              type=click.File(mode='r', encoding='utf-8-sig'))
def yaml_sample(log_level, yaml_file, other_yaml_file):
    """YAML sample code."""
    logging.basicConfig(level=_LOG_LEVEL_MAP[log_level])
    yaml_sample_obj = yaml.load(stream=yaml_file, Loader=yaml.SafeLoader)
    key_list = traverse_yaml_key_dfs(node=yaml_sample_obj)
    logging.info(key_list)
    key_list = traverse_yaml_key_bfs(node=yaml_sample_obj)
    logging.info(key_list)
    value_list = traverse_yaml_value(node=yaml_sample_obj)
    logging.info(value_list)
    if other_yaml_file is not None:
        other_yaml_obj = yaml.load(
            stream=other_yaml_file, Loader=yaml.SafeLoader)
        ret = compare_yaml(from_node=yaml_sample_obj, to_node=other_yaml_obj)
        logging.info(ret)


if __name__ == "__main__":
    yaml_sample()  # pylint: disable=no-value-for-parameter
