import React, { useContext} from "react";
import { Menu } from "antd";
import {
  BulbOutlined,
  BellOutlined,
  GlobalOutlined,
  EnterOutlined,
  GoogleCircleFilled,
} from "@ant-design/icons";
import SettingsContext from "../../../context/settings-context";
import { useTranslation } from "react-i18next";
import { auth, provider, getCurrentUserDetails, signInWithPopup } from "../../../utils/firebase-config";

const UserProfilePopover = () => {
  const {colorTheme, locale, toggleTheme, changeLocale} = useContext(SettingsContext);
  let user = localStorage.getItem("user");
  console.log("User", user);
  const { t } = useTranslation();

  const handleLogin = async () => {
    try {
      const result = await signInWithPopup(auth, provider);
      user = result.user;
      console.log("User logged in", user);
      localStorage.setItem("authToken", user.accessToken);

      const response = await getCurrentUserDetails();
      localStorage.setItem("user", JSON.stringify(response));
      console.log("Response from backend", response);
      window.location.reload();
    } catch (error) {
      console.error("Error during login", error);
    }
  }

  const handleLogout = async () => {
    try {
      await auth.signOut();
      localStorage.removeItem("user");
      window.location.reload();
    }
    catch (error) {
      console.error("Error during logout", error);
    }
  }


  return (
    <Menu className="user-profile-menu" mode="inline">
      {user ? 
        <Menu.Item key="1" className="profile-item">
        <strong>{t('header.profile-link')}</strong>
        </Menu.Item>
        :
        <Menu.Item key="1" onClick={handleLogin} icon={<GoogleCircleFilled/>} className="profile-item">
        <strong>{t('header.login-link')}</strong>
      </Menu.Item>
      }
      
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
      {user ?
        <Menu.Item key="5" onClick={handleLogout} danger icon={<EnterOutlined />}>
          {t('header.logout-link')}
        </Menu.Item>
        :""
      }
     
    </Menu>
  );
};

export default UserProfilePopover;
