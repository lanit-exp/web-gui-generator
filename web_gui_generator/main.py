from mako.lookup import TemplateLookup
from selenium import webdriver

import fileproc as fp
from web_gui_generator import PROJ_ROOT_DIR, TREES_PATH
from web_gui_generator.model.w_descr_holder import DescrHolder
from web_gui_generator.model.w_geom import WidgetObjectGeometryFactory
from web_gui_generator.model.wo_concr import WOFactory

HTML_TEMPLATES_DIR = PROJ_ROOT_DIR / "resources/templates/html"
CSS_TEMPLATES_DIR = PROJ_ROOT_DIR / "resources/templates/css"
DRIVER = PROJ_ROOT_DIR / "driver/chromedriver.exe"
OUTPUT_DIR = PROJ_ROOT_DIR / "otp"

if __name__ == '__main__':
    trees = fp.Reader.read_trees(TREES_PATH, 5, start=1)
    with webdriver.Chrome(DRIVER) as driver:
        fp.Writer.write_names(OUTPUT_DIR / "labels.names", DescrHolder.get_instance().widget_names)
        for i, tree in enumerate(trees):
            print(tree)
            html_file_otp = OUTPUT_DIR / f"index-{i + 1}.html"
            css_file_otp = OUTPUT_DIR / f"style-{i + 1}.css"
            screenshot_otp = OUTPUT_DIR / f"screenshot-{i + 1}.png"
            geom_otp = OUTPUT_DIR / f"geometry-{i + 1}.txt"

            WOFactory.reset_ids()
            root_wo = WOFactory.create_from_tree(tree)
            lookup = TemplateLookup(directories=[HTML_TEMPLATES_DIR])
            with open(html_file_otp, 'w') as outfile:
                outfile.write(lookup.get_template("LWindow.mako")
                              .render(root_node=root_wo, lookup=lookup, css_file=css_file_otp.name))

            lookup = TemplateLookup(directories=[CSS_TEMPLATES_DIR])
            with open(css_file_otp, 'w') as outfile:
                outfile.write(lookup.get_template("style.mako").render(root_node=root_wo, lookup=lookup))

            driver.get(str(html_file_otp))
            driver.save_screenshot(str(screenshot_otp))

            wo_with_geoms_list = WidgetObjectGeometryFactory.create_from_tree(root_wo, driver)
            for w_geom in wo_with_geoms_list.list_:
                fp.Writer.write_geom(geom_otp, str(w_geom))

