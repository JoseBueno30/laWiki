import React, { useContext, useState } from "react";
import { Menu } from "antd";
import {
  BulbOutlined,
  BellOutlined,
  GlobalOutlined,
  EnterOutlined,
} from "@ant-design/icons";
import SettingsContext from "../../../context/settings-context";
import { useTranslation } from "react-i18next";

const UserProfilePopover = () => {
  const {colorTheme, locale, toggleTheme, changeLocale} = useContext(SettingsContext);
  const [notifications, setNotifications] = useState("Email");
  const { t } = useTranslation();

  return (
    <Menu className="user-profile-menu" mode="inline">
      <Menu.Item key="1" className="profile-item">
        <strong>{t('header.profile-link')}</strong>
      </Menu.Item>
      <Menu.Divider />
      <Menu.SubMenu
        key="2"
        title={t('header.theme-menu', {theme: colorTheme == "light" ? t('header.theme-light') : t('header.theme-dark')})}
        icon={<BulbOutlined />}
      >
        <Menu.Item key="2-1" onClick={() => toggleTheme("light")}>
          {t('header.theme-light')}
        </Menu.Item>
        <Menu.Item key="2-2" onClick={() => toggleTheme("dark")}>
          {t('header.theme-dark')}
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.SubMenu
        key="3"
        title={t('header.notifications-menu', {notifications: notifications == "Email" ? t('header.notifications-email') : t('header.notifications-afterlogin')})}
        icon={<BellOutlined />}
      >
        <Menu.Item key="3-1" onClick={() => setNotifications("Email")}>
          {t('header.notifications-email')}
        </Menu.Item>
        <Menu.Item key="3-2" onClick={() => setNotifications("After login")}>
          {t('header.notifications-afterlogin')}
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.SubMenu
        key="4"
        title={t('header.language-menu', {language: locale == "en" ? t('header.language-en') : locale == "es" ? t('header.language-es') : t('header.language-fr')})}
        icon={<GlobalOutlined />}
      >
        <Menu.Item key="4-1" onClick={() => changeLocale("en")}>
          {t('header.language-en')}
        </Menu.Item>
        <Menu.Item key="4-2" onClick={() => changeLocale("es")}>
          {t('header.language-es')}
        </Menu.Item>
        <Menu.Item key="4-3" onClick={() => changeLocale("fr")}>
          {t('header.language-fr')}
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.Divider />
      <Menu.Item key="5" danger icon={<EnterOutlined />}>
        {t('header.logout-link')}
      </Menu.Item>
    </Menu>
  );
};

export default UserProfilePopover;
