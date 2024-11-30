import React, { useContext, useState } from "react";
import { Menu } from "antd";
import {
  BulbOutlined,
  BellOutlined,
  GlobalOutlined,
  EnterOutlined,
} from "@ant-design/icons";
import { ThemeContext } from "../../../context/theme-context";
import { useTranslation } from "react-i18next";

const UserProfilePopover = () => {
  const {colorTheme, locale, toggleTheme, changeLocale} = useContext(ThemeContext);
  const [notifications, setNotifications] = useState("Email");
  const { t } = useTranslation('header-trans');

  return (
    <Menu className="user-profile-menu" mode="inline">
      <Menu.Item key="1" className="profile-item">
        <strong>{t('profile-link')}</strong>
      </Menu.Item>
      <Menu.Divider />
      <Menu.SubMenu
        key="2"
        title={t('theme-menu', {theme: colorTheme == "light" ? t('theme-light') : t('theme-dark')})}
        icon={<BulbOutlined />}
      >
        <Menu.Item key="2-1" onClick={toggleTheme}>
          {colorTheme === "light" ? "Switch to Dark" : "Switch to Light"}
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.SubMenu
        key="3"
        title={t('notifications-menu', {notifications: notifications == "Email" ? t('notifications-email') : t('notifications-afterlogin')})}
        icon={<BellOutlined />}
      >
        <Menu.Item key="3-1" onClick={() => setNotifications("Email")}>
          {t('notifications-email')}
        </Menu.Item>
        <Menu.Item key="3-2" onClick={() => setNotifications("After login")}>
          {t('notifications-afterlogin')}
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.SubMenu
        key="4"
        title={t('language-menu', {language: locale == "en" ? t('language-en') : locale == "es" ? t('language-es') : t('language-fr')})}
        icon={<GlobalOutlined />}
      >
        <Menu.Item key="4-1" onClick={() => changeLocale("en")}>
          {t('language-en')}
        </Menu.Item>
        <Menu.Item key="4-2" onClick={() => changeLocale("es")}>
          {t('language-es')}
        </Menu.Item>
        <Menu.Item key="4-3" onClick={() => changeLocale("fr")}>
          {t('language-fr')}
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.Divider />
      <Menu.Item key="5" danger icon={<EnterOutlined />}>
        {t('logout-link')}
      </Menu.Item>
    </Menu>
  );
};

export default UserProfilePopover;
