#!/usr/bin/env python2
# -*- coding: utf8 -*-
#
#  Copyright (c) 2014, 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Jesse Griffin <jesse@distantshores.org>
#  Phil Hopper <phillip_hopper@wycliffeassociates.org>

import inspect
import os
import codecs
import sys
import urllib2
import re
import json
import getopt
import shutil

# use a path relative to the current file rather than a hard-coded path
current_dir = os.path.dirname(inspect.stack()[0][1])
sys.path.append(current_dir)

source_dir = os.path.dirname(os.path.dirname(current_dir))
destination_dir = os.path.join(source_dir, '_site')
index_template_file = ''
catalog_api_url = u'http://cdn.door43.org/obs/txt/1/obs-catalog.json'
language_api_url = u'http://cdn.door43.org/obs/txt/1/{0}/obs-{0}.json'
image_api_url = 'https://cdn.door43.org/obs/jpg'

unfolding_word_dir = '/var/www/vhosts/api.unfoldingword.org/httpdocs/obs/txt/1/'

# HTML templates
frame_template = u'<section data-background="{0}"><p>{1}</p></section>'
next_link_template = u'<section><a href="../{0}/index.html"><p>{1}</p></a></section>'
# to include literal braces in a format string, double them
menu_link_template = u'<li><a href="../{0}/{{{{ PATH_INDEX }}}}">{1}</a></li>'
# noinspection SpellCheckingInspection
title_template = u'''<section><h1>{0}</h1><h3>{1}</h3><div class="uwchecking"></div>
    <a href="https://unfoldingword.bible/quality/" target="_blank">
        <img alt="checking icon" src="https://api.unfoldingword.org/obs/jpg/1/checkinglevels/uW-Level{2}-64px.png" />
    </a>
</section>'''

# template regex - uses Blade/Twig syntax
LANG_CODE_REGEX = re.compile(r"(\{{2}\s*LANG_CODE\s*\}{2})", re.DOTALL)
MENY_REGEX = re.compile(r"(\{{2}\s*MENY\s*\}{2})", re.DOTALL)
REVEAL_SLIDES_REGEX = re.compile(r"(\{{2}\s*REVEAL_SLIDES\s*\}{2})", re.DOTALL)

# paths for local and web files
PATH_INDEX_REGEX = re.compile(r"(\{{2}\s*PATH_INDEX\s*\}{2})", re.DOTALL)
# PATH_CSS_REGEX = re.compile(r"(\{{2}\s*PATH_CSS\s*\}{2})", re.DOTALL)
# PATH_JS_REGEX = re.compile(r"(\{{2}\s*PATH_JS\s*\}{2})", re.DOTALL)

# list layout [RegularExpression, LocalPath, WebPath]
res_paths = [[PATH_INDEX_REGEX, u'index.html', u'']]


def build_reveal(out_dir, lang_data, html_template, check_lev):
    """
    Builds reveal.js presentation for the given language.
    """
    lang = lang_data['language']
    resolutions = ['360px', '2160px']
    next_story = lang_data['app_words']['next_chapter']
    chapters = get_chapters(lang_data['chapters'])
    meny = get_menu(chapters)

    for res in resolutions:
        num_chapters = len(lang_data['chapters'])

        for i in range(1, num_chapters + 1):
            c = lang_data['chapters'][i - 1]

            page = []
            chapter_num = c['number'].strip('.txt')

            # the title slide
            page.append(title_template.format(c['title'], c['ref'], check_lev))

            # a slides for each frame
            for f in c['frames']:
                img_url = get_img_url(res, f['id'])
                page.append(frame_template.format(img_url, f['text']))

            # a slide that links to the next story
            if i < num_chapters:
                page.append(next_link_template.format(str(i + 1).zfill(2), next_story))

            # put it together
            html = MENY_REGEX.sub(meny, html_template)
            html = REVEAL_SLIDES_REGEX.sub('\n'.join(page), html)
            html = LANG_CODE_REGEX.sub(lang, html)

            # save the html
            output_file = os.path.join(out_dir, res, chapter_num, 'index.html')
            write_template(output_file, html)


def get_chapters(chapters):
    """
    Returns list of chapters.
    """
    return [c['title'] for c in chapters]


def get_menu(chapters):
    """
    Returns an HTML list formatted string of the chapters with links.
    """
    menu = []
    i = 1
    for c in chapters:
        menu.append(menu_link_template.format(str(i).zfill(2), c))
        i += 1
    return u'\n        '.join(menu)


def write_template(output_file, page):
    """
    Writes out two versions, one for web viewer and one for local viewer.
    """
    # list layout [RegularExpression, LocalPath, WebPath]
    for itm in res_paths:
        page = itm[0].sub(itm[1], page)

    write_file(output_file, page)


def get_img_url(res, fid):
    global image_api_url
    return '{0}/{1}/obs-en-{2}.jpg'.format(image_api_url, res, fid)


def read_file(infile):
    f = codecs.open(infile, 'r', encoding='utf-8').read()
    return f


def write_file(outfile, page):
    make_dir(outfile.rpartition('/')[0])
    f = codecs.open(outfile, 'w', encoding='utf-8')
    f.write(page)
    f.close()


def make_dir(d):
    if not os.path.exists(d):
        os.makedirs(d, 0755)


def load_json(f, t):
    if os.path.isfile(f):
        return json.load(codecs.open(f, 'r', encoding='utf-8'))
    if t == 'd':
        return json.loads('{}')
    else:
        return json.loads('[]')


def get_url(url):
    # noinspection PyBroadException
    try:
        request = urllib2.urlopen(url).read()
        return request
    except:
        print '  => ERROR retrieving {0}\nCheck the URL'.format(url)


# Get the arguments passed to the script
# @param array argv The arguments passed in the script minus the script name
#
def get_arguments(argv):
    # Call global to modify vars
    global source_dir, destination_dir
    try:
        opts, args = getopt.getopt(argv, 'hs:d:', ['help', 'source=', 'destination='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-s', '--source'):
            source_dir = arg
        elif opt in ('-d', '--destination'):
            destination_dir = arg


def usage():
    print ''
    print 'Usage:'
    print '     generate_script.py [options]'
    print 'Options:'
    print '     -s --source [DIR] Source directory (default: {0})'.format(source_dir)
    print '     -d --destination [DIR] Destination directory (default: {0})'.format(destination_dir)
    print '     -h --help Show this message'
    print ''


def export():
    cat = json.loads(get_url(catalog_api_url))
    template = read_file(index_template_file)
    for x in cat:
        lang = x['language']
        slide_directory = os.path.join(destination_dir, lang, 'slides')

        # Remove the current slides directory if it exists
        if os.path.exists(slide_directory):
            shutil.rmtree(slide_directory)

        lang_json = json.loads(get_url(language_api_url.format(lang)))
        print '* Building the slide shows for {0}'.format(lang)
        build_reveal(slide_directory, lang_json, template, x['status']['checking_level'])


if __name__ == '__main__':
    get_arguments(sys.argv[1:])
    print 'Using source directory: {0}'.format(source_dir)
    print 'Using destination directory: {0}'.format(destination_dir)
    index_template_file = os.path.join(source_dir, '_layouts/language_slideshow.html')
    export()
