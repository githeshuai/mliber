# -*- coding:utf-8 -*-

from apply_widget_ui import ApplyWidgetUI
import mliber_global


class ApplyWidget(ApplyWidgetUI):
    def __init__(self, parent=None):
        super(ApplyWidget, self).__init__(parent)

    def set_asset(self, asset):
        """
        接口
        :param asset: <Asset>
        :return:
        """
        self.element_list_view.set_asset(asset)
        asset_id = asset.id
        name = asset.name
        created_by = asset.created_by
        created_at = asset.created_at
        tag_names = [tag.name for tag in asset.tags]
        description = asset.description
        elements = asset.elements
        self._set_id(asset_id)
        self._set_name(name)
        self._set_created_by(created_by)
        self._set_created_at(created_at)
        self._set_tag(tag_names)
        self._set_description(description)
        self._set_element(elements)

    def _set_id(self, asset_id):
        """
        :param asset_id: <int>
        :return:
        """
        self.id_le.setText(str(asset_id))

    def _set_name(self, name):
        """
        :param name: <str>
        :return:
        """
        self.name_le.setText(name)

    def _set_created_by(self, user_id):
        """
        :param user_id: <int>
        :return:
        """
        with mliber_global.db() as db:
            user = db.find_one("User", [["id", "=", user_id], ["status", "=", "Active"]])
            if user:
                self.created_by_le.setText(user.name)

    def _set_created_at(self, created_at):
        """
        :param created_at:
        :return:
        """
        if created_at:
            create_at_str = created_at.strftime("%Y-%m-%d,%H:%M:%S")
            self.created_at_le.setText(create_at_str)

    def _set_tag(self, tag_names):
        """
        :param tag_names: <list>
        :return:
        """
        if tag_names:
            self.tag_widget.add_tags(tag_names)

    def _set_description(self, description):
        """
        :param description: <str>
        :return:
        """
        if description:
            self.description_te.setText(description)

    def _set_element(self, elements):
        """
        :param elements: <list> [Element.....]
        :return:
        """
        if elements:
            self.element_list_view.set_elements(elements)
