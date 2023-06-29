import os
import re
from jinja2 import Environment, FileSystemLoader


# helper function to get paths for the given group of templates. Paths will be passed to each universe template.
def get_paths(universe, group_name):
    group_dir = os.path.join('templates', universe, group_name)
    group_paths = [os.path.join(universe, group_name, file) for file in os.listdir(group_dir) if file.endswith('.html')]
    group_paths = sorted(group_paths, key=extract_range)
    return group_paths

# Helper function get the strategy range from each filename.
# TODO: deprecated - remove
def extract_range(filename):
    # Extracts the range suffix from the filename (e.g. '1-5' from 'file_1-5.html')
    match = re.search(r'(\d+-\d+)', filename)
    if match:
        return tuple(map(int, match.group(1).split('-')))
    return (0, 0)

def sort_by_range(paths):
    """Sort the list of paths based on the range in their filenames."""
    def extract_range(filename):
        match = re.search(r'(\d+)-(\d+)', filename)
        return tuple(map(int, match.groups())) if match else (0, 0)

    return sorted(paths, key=lambda p: extract_range(os.path.basename(p)))


def build_template_objects(paths, group_name, benchAttr=False):
    templates = []
    for index, path in enumerate(paths):
        filename = os.path.basename(path)
        rng = filename.split('_')[0] if '_' in filename else filename.split('.')[0]
        template = {
            'path': path,
            'groupname': group_name,
            'filename': filename,
            'range': rng,
            'index': index
        }
        if benchAttr:
            template['benchtype'] = 'synth' if '_s' in filename else 'index'
        templates.append(template)
    
    return templates


# Helper function to build a datastructure for every template group
def build_template_group(universe, group_name, benchAttr=False):
    group = []

    group_dir = os.path.join('templates', universe, group_name)
    group_paths = [os.path.join(universe, group_name, file) for file in os.listdir(group_dir) if file.endswith('.html')]

    # Split paths by index benchmark and synth benchmark if needed
    group_s_paths = []
    if benchAttr:
        group_i_paths = []
        for path in group_paths:
            if '_s' in os.path.basename(path):
                group_s_paths.append(path)
            else:
                group_i_paths.append(path)
            group_paths = group_i_paths
    
    # Build a template object for each path
    group_paths = sort_by_range(group_paths)
    group = build_template_objects(group_paths, group_name, benchAttr)
    if benchAttr:
        group_s_paths = sort_by_range(group_s_paths)
        group = group + build_template_objects(group_s_paths, group_name, benchAttr)

    return group
            

        


### TEMPLATING BEGINS ###

# this tells jinja2 to look for templates
# in the templates subdirectory
env = Environment(
    loader = FileSystemLoader('templates'),
)

# universes = [u for u in os.listdir('templates') if os.path.isdir(os.path.join('templates', u))]
universes = ['SP500', 'SPNEW', 'N100', 'NKY', 'SASEID']
rendered_universes = []

# Get universe template and render it for each respective universe.
for universe in universes:
    universe_template_path = os.path.join('templates', universe, f'{universe}-template.html')
    if os.path.exists(universe_template_path):
        table_templates = build_template_group(universe, 'table', benchAttr=True)
        pnl_templates = build_template_group(universe, 'pnl', benchAttr=False)
        dnpnl_templates = build_template_group(universe, 'dnpnl', benchAttr=True)


        # Check that the number of paths found are the same
        # paths = [pnl_paths, table_paths]
        # if not all(len(p) == len(pnl_paths) for p in paths):
        #     print(f'Error: The number of files in each template folder are not equal for universe: {universe}')
        #     exit(1)
        

        # render the template.
        # in other words, we replace the template tag by the contents of the overfitting file
        universe_template = env.get_template(os.path.join(universe, f'{universe}-template.html'))
        rendered_universe = universe_template.render(
            universe=universe,
            pnl_templates=pnl_templates,
            dnpnl_templates=dnpnl_templates,
            table_templates=table_templates
            )
        rendered_universes.append(rendered_universe)
    else:
        print(f'No template found for universe {universe}')


# Now render the main index-template.html by injecting the rendered universe templates
index_template = env.get_template('index-template.html')
rendered_index = index_template.render(universes=rendered_universes)

# write the rendered index.html to disk
with open('index.html', 'w') as ofile:
    ofile.write(rendered_index)