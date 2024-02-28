# -*- coding: utf-8 -*-
#
# The Linux Kernel documentation build configuration file, created by
# sphinx-quickstart on Fri Feb 12 13:51:46 2016.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import sphinx
import shutil

# helper
# ------

def have_command(cmd):
    """Search ``cmd`` in the ``PATH`` environment.

    If found, return True.
    If not found, return False.
    """
    return shutil.which(cmd) is not None

# Get Sphinx version
major, minor, patch = sphinx.version_info[:3]

#
# Warn about older versions that we don't want to support for much
# longer.
#
if (major < 2) or (major == 2 and minor < 4):
    print('WARNING: support for Sphinx < 2.4 will be removed soon.')

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('sphinx'))
from load_config import loadConfig

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '2.4.4'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['kerneldoc', 'rstFlatTable', 'kernel_include',
              'kfigure', 'sphinx.ext.ifconfig', 'automarkup',
              'maintainers_include', 'sphinx.ext.autosectionlabel',
              'kernel_abi', 'kernel_feat', 'translations']

if major >= 3:
    if (major > 3) or (minor > 0 or patch >= 2):
        # Sphinx c function parser is more pedantic with regards to type
        # checking. Due to that, having macros at c:function cause problems.
        # Those needed to be scaped by using c_id_attributes[] array
        c_id_attributes = [
            # GCC Compiler types not parsed by Sphinx:
            "__restrict__",

            # include/linux/compiler_types.h:
            "__iomem",
            "__kernel",
            "noinstr",
            "notrace",
            "__percpu",
            "__rcu",
            "__user",
            "__force",

            # include/linux/compiler_attributes.h:
            "__alias",
            "__aligned",
            "__aligned_largest",
            "__always_inline",
            "__assume_aligned",
            "__cold",
            "__attribute_const__",
            "__copy",
            "__pure",
            "__designated_init",
            "__visible",
            "__printf",
            "__scanf",
            "__gnu_inline",
            "__malloc",
            "__mode",
            "__no_caller_saved_registers",
            "__noclone",
            "__nonstring",
            "__noreturn",
            "__packed",
            "__pure",
            "__section",
            "__always_unused",
            "__maybe_unused",
            "__used",
            "__weak",
            "noinline",
            "__fix_address",
            "__counted_by",

            # include/linux/memblock.h:
            "__init_memblock",
            "__meminit",

            # include/linux/init.h:
            "__init",
            "__ref",

            # include/linux/linkage.h:
            "asmlinkage",

            # include/linux/btf.h
            "__bpf_kfunc",
        ]

else:
    extensions.append('cdomain')

# Ensure that autosectionlabel will produce unique names
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2

# Load math renderer:
# For html builder, load imgmath only when its dependencies are met.
# mathjax is the default math renderer since Sphinx 1.8.
have_latex =  have_command('latex')
have_dvipng = have_command('dvipng')
load_imgmath = have_latex and have_dvipng

# Respect SPHINX_IMGMATH (for html docs only)
if 'SPHINX_IMGMATH' in os.environ:
    env_sphinx_imgmath = os.environ['SPHINX_IMGMATH']
    if 'yes' in env_sphinx_imgmath:
        load_imgmath = True
    elif 'no' in env_sphinx_imgmath:
        load_imgmath = False
    else:
        sys.stderr.write("Unknown env SPHINX_IMGMATH=%s ignored.\n" % env_sphinx_imgmath)

# Always load imgmath for Sphinx <1.8 or for epub docs
load_imgmath = (load_imgmath or (major == 1 and minor < 8)
                or 'epub' in sys.argv)

if load_imgmath:
    extensions.append("sphinx.ext.imgmath")
    math_renderer = 'imgmath'
else:
    math_renderer = 'mathjax'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['sphinx/templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'The Linux Kernel'
copyright = 'The kernel development community'
author = 'The kernel development community'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# In a normal build, version and release are are set to KERNELVERSION and
# KERNELRELEASE, respectively, from the Makefile via Sphinx command line
# arguments.
#
# The following code tries to extract the information by reading the Makefile,
# when Sphinx is run directly (e.g. by Read the Docs).
try:
    makefile_version = None
    makefile_patchlevel = None
    for line in open('../Makefile'):
        key, val = [x.strip() for x in line.split('=', 2)]
        if key == 'VERSION':
            makefile_version = val
        elif key == 'PATCHLEVEL':
            makefile_patchlevel = val
        if makefile_version and makefile_patchlevel:
            break
except:
    pass
finally:
    if makefile_version and makefile_patchlevel:
        version = release = makefile_version + '.' + makefile_patchlevel
    else:
        version = release = "unknown version"

#
# HACK: there seems to be no easy way for us to get at the version and
# release information passed in from the makefile...so go pawing through the
# command-line options and find it for ourselves.
#
def get_cline_version():
    c_version = c_release = ''
    for arg in sys.argv:
        if arg.startswith('version='):
            c_version = arg[8:]
        elif arg.startswith('release='):
            c_release = arg[8:]
    if c_version:
        if c_release:
            return c_version + '-' + c_release
        return c_version
    return version # Whatever we came up with before

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['output']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

primary_domain = 'c'
highlight_language = 'none'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# Default theme
html_theme = 'alabaster'
html_css_files = []

if "DOCS_THEME" in os.environ:
    html_theme = os.environ["DOCS_THEME"]

if html_theme == 'sphinx_rtd_theme' or html_theme == 'sphinx_rtd_dark_mode':
    # Read the Docs theme
    try:
        import sphinx_rtd_theme
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

        # Add any paths that contain custom static files (such as style sheets) here,
        # relative to this directory. They are copied after the builtin static files,
        # so a file named "default.css" will overwrite the builtin "default.css".
        html_css_files = [
            'theme_overrides.css',
        ]

        # Read the Docs dark mode override theme
        if html_theme == 'sphinx_rtd_dark_mode':
            try:
                import sphinx_rtd_dark_mode
                extensions.append('sphinx_rtd_dark_mode')
            except ImportError:
                html_theme == 'sphinx_rtd_theme'

        if html_theme == 'sphinx_rtd_theme':
                # Add color-specific RTD normal mode
                html_css_files.append('theme_rtd_colors.css')

        html_theme_options = {
            'navigation_depth': -1,
        }

    except ImportError:
        html_theme = 'alabaster'

if "DOCS_CSS" in os.environ:
    css = os.environ["DOCS_CSS"].split(" ")

    for l in css:
        html_css_files.append(l)

if major <= 1 and minor < 8:
    html_context = {
        'css_files': [],
    }

    for l in html_css_files:
        html_context['css_files'].append('_static/' + l)

if  html_theme == 'alabaster':
    html_theme_options = {
        'description': get_cline_version(),
        'page_width': '65em',
        'sidebar_width': '15em',
        'fixed_sidebar': 'true',
        'font_size': 'inherit',
        'font_family': 'serif',
    }

sys.stderr.write("Using %s theme\n" % html_theme)

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['sphinx-static']

# If true, Docutils "smart quotes" will be used to convert quotes and dashes
# to typographically correct entities.  This will convert "--" to "—",
# which is not always what we want, so disable it.
smartquotes = False

# Custom sidebar templates, maps document names to template names.
# Note that the RTD theme ignores this
html_sidebars = { '**': ['searchbox.html', 'kernel-toc.html', 'sourcelink.html']}

# about.html is available for alabaster theme. Add it at the front.
if html_theme == 'alabaster':
    html_sidebars['**'].insert(0, 'about.html')

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = 'images/logo.svg'

# Output file base name for HTML help builder.
htmlhelp_basename = 'TheLinuxKerneldoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '11pt',

    # Latex figure (float) alignment
    #'figure_align': 'htbp',

    # Don't mangle with UTF-8 chars
    'inputenc': '',
    'utf8extra': '',

    # Set document margins
    'sphinxsetup': '''
        hmargin=0.5in, vmargin=1in,
        parsedliteralwraps=true,
        verbatimhintsturnover=false,
    ''',

    #
    # Some of our authors are fond of deep nesting; tell latex to
    # cope.
    #
    'maxlistdepth': '10',

    # For CJK One-half spacing, need to be in front of hyperref
    'extrapackages': r'\usepackage{setspace}',

    # Additional stuff for the LaTeX preamble.
    'preamble': '''
        % Use some font with UTF-8 support with XeLaTeX
        \\usepackage{fontspec}
        \\setsansfont{DejaVu Sans}
        \\setromanfont{DejaVu Serif}
        \\setmonofont{DejaVu Sans Mono}
    ''',
}

# Fix reference escape troubles with Sphinx 1.4.x
if major == 1:
    latex_elements['preamble']  += '\\renewcommand*{\\DUrole}[2]{ #2 }\n'


# Load kerneldoc specific LaTeX settings
latex_elements['preamble'] += '''
        % Load kerneldoc specific LaTeX settings
	\\input{kerneldoc-preamble.sty}
'''

# With Sphinx 1.6, it is possible to change the Bg color directly
# by using:
#	\definecolor{sphinxnoteBgColor}{RGB}{204,255,255}
#	\definecolor{sphinxwarningBgColor}{RGB}{255,204,204}
#	\definecolor{sphinxattentionBgColor}{RGB}{255,255,204}
#	\definecolor{sphinximportantBgColor}{RGB}{192,255,204}
#
# However, it require to use sphinx heavy box with:
#
#	\renewenvironment{sphinxlightbox} {%
#		\\begin{sphinxheavybox}
#	}
#		\\end{sphinxheavybox}
#	}
#
# Unfortunately, the implementation is buggy: if a note is inside a
# table, it isn't displayed well. So, for now, let's use boring
# black and white notes.

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
# Sorted in alphabetical order
latex_documents = [
]

# Add all other index files from Documentation/ subdirectories
for fn in os.listdir('.'):
    doc = os.path.join(fn, "index")
    if os.path.exists(doc + ".rst"):
        has = False
        for l in latex_documents:
            if l[0] == doc:
                has = True
                break
        if not has:
            latex_documents.append((doc, fn + '.tex',
                                    'Linux %s Documentation' % fn.capitalize(),
                                    'The kernel development community',
                                    'manual'))

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True

# Additional LaTeX stuff to be copied to build directory
latex_additional_files = [
    'sphinx/kerneldoc-preamble.sty',
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'thelinuxkernel', 'The Linux Kernel Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'TheLinuxKernel', 'The Linux Kernel Documentation',
     author, 'TheLinuxKernel', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for Epub output ----------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

#=======
# rst2pdf
#
# Grouping the document tree into PDF files. List of tuples
# (source start file, target name, title, author, options).
#
# See the Sphinx chapter of https://ralsina.me/static/manual.pdf
#
# FIXME: Do not add the index file here; the result will be too big. Adding
# multiple PDF files here actually tries to get the cross-referencing right
# *between* PDF files.
pdf_documents = [
    ('kernel-documentation', u'Kernel', u'Kernel', u'J. Random Bozo'),
]

# kernel-doc extension configuration for running Sphinx directly (e.g. by Read
# the Docs). In a normal build, these are supplied from the Makefile via command
# line arguments.
kerneldoc_bin = '../scripts/kernel-doc'
kerneldoc_srctree = '..'

# ------------------------------------------------------------------------------
# Since loadConfig overwrites settings from the global namespace, it has to be
# the last statement in the conf.py file
# ------------------------------------------------------------------------------
loadConfig(globals())
