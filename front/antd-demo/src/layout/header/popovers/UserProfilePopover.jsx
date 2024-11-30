import React, { useContext, useState } from "react";
import { Menu } from "antd";
import {
  BulbOutlined,
  BellOutlined,
  GlobalOutlined,
  EnterOutlined,
} from "@ant-design/icons";
import { ThemeContext } from "../../../context/theme-context";

const UserProfilePopover = () => {
  const {colorTheme, locale, toggleTheme, changeLocale} = useContext(ThemeContext);
  const [notifications, setNotifications] = useState("Email");

  return (
    <Menu className="user-profile-menu" mode="inline">
      <Menu.Item key="1" className="profile-item">
        <strong>See profile</strong>
      </Menu.Item>
      <Menu.Divider />
      <Menu.SubMenu
        key="2"
        title={`Theme: ${colorTheme === "light" ? "Light" : "Dark"}`}
        icon={<BulbOutlined />}
      >
        <Menu.Item key="2-1" onClick={toggleTheme}>
          {colorTheme === "light" ? "Switch to Dark" : "Switch to Light"}
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.SubMenu
        key="3"
        title={`Notifications: ${notifications}`}
        icon={<BellOutlined />}
      >
        <Menu.Item key="3-1" onClick={() => setNotifications("Email")}>
          Email
        </Menu.Item>
        <Menu.Item key="3-2" onClick={() => setNotifications("After login")}>
          After login
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.SubMenu
        key="4"
        title={`Language: ${locale}`}
        icon={<GlobalOutlined />}
      >
        <Menu.Item key="4-1" onClick={() => changeLocale("en")}>
          English
        </Menu.Item>
        <Menu.Item key="4-2" onClick={() => changeLocale("es")}>
          Español
        </Menu.Item>
        <Menu.Item key="4-3" onClick={() => changeLocale("fr")}>
          Français
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.Divider />
      <Menu.Item key="5" danger icon={<EnterOutlined />}>
        Log out
      </Menu.Item>
    </Menu>
  );
};

export default UserProfilePopover;
