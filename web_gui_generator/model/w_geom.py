from typing import Tuple, List

from selenium.webdriver.chrome.webdriver import WebDriver

from web_gui_generator.model.utils import Utils
from web_gui_generator.model.w_descr_holder import DescrHolder
from web_gui_generator.model.wo_abc import WOUnion, ContCompWOUnion, WOMixin


class Geometry(object):
    def __init__(self, height: int, width: int, x: float, y: float):
        self._w = width
        self._h = height
        self._x = x
        self._y = y

    @property
    def w(self) -> int:
        return self._w

    @property
    def h(self) -> int:
        return self._h

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def location(self) -> Tuple[float, float]:
        return self._x, self._y

    @property
    def size(self) -> [int, int]:
        return self._w, self._h

    def coco_repr(self):
        return f"{self._x} {self._y} {self._w} {self._h}"

    def __repr__(self):
        return self.coco_repr()


class WidgetObjectWithGeometry(object):
    def __init__(self, widget_object: WOMixin, geometry: Geometry):
        self.widget_object = widget_object
        self.name_number = DescrHolder.get_instance().get_widget_name_number(
            widget_object.name)
        self.geometry = geometry

    def __repr__(self):
        return f"<WidgetObjectGeometry: wo: {self.widget_object}; " \
               f"wo_geom: {self.geometry}>"

    def __str__(self):
        return f"{self.widget_object.name} {self.geometry}"


class WidgetObjectWithGeometryList(object):
    def __init__(self, wo_with_geometry_list: list[WidgetObjectWithGeometry]):
        self.list_ = wo_with_geometry_list


class WidgetObjectGeometryFactory(object):
    @classmethod
    def create_from_tree(cls, root_wo: ContCompWOUnion, driver: WebDriver) \
            -> WidgetObjectWithGeometryList:
        list_ = GeomExtraction.extract_tree_geometries(root_wo, driver)
        return WidgetObjectWithGeometryList(list_)


class GeomExtraction(object):
    @classmethod
    def extract_geometry(cls, wo: WOUnion, driver: WebDriver):
        return Geometry(**driver.find_element_by_id(wo.id_).rect)

    @classmethod
    def extract_tree_geometries(cls, root_wo: ContCompWOUnion, driver: WebDriver) \
            -> List[WidgetObjectWithGeometry]:
        hook = lambda wo: WidgetObjectWithGeometry(wo, cls.extract_geometry(wo, driver))
        return Utils.dfs(root_wo, hook)
