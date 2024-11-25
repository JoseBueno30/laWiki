import {
  Flex,
  Input,
  Button,
  Badge,
  Avatar,
  Popover,
  Menu,
} from "antd";
import React, { useContext, useState } from "react";
import { ThemeContext } from "../../context/theme-context";
import {
  ControlOutlined,
  PlusOutlined,
  BellOutlined,
  UserOutlined,
} from "@ant-design/icons";
import PropTypes from "prop-types";
import "./PageHeader.css";
import Title from "antd/es/typography/Title";
import { Link } from "react-router-dom";

const FilterIcon = () => {
  return (
    <div className="icon-container" onClick={FilterClickHandler}>
      <ControlOutlined style={{ fontSize: "24px" }} />
    </div>
  );
};

const AddIcon = () => <PlusOutlined />;

const NotificationsClickHandler = () => {
  console.log("Notifications clicked");
};

const FilterClickHandler = () => {
  console.log("Filter clicked");
};

const LaWikiClickHandler = () => {
  console.log("LaWiki clicked");
};

const WikiClickHandler = () => {
  console.log("Wiki clicked");
};

const WikiHeader = () => {
  const { colorTheme, toggleTheme } = useContext(ThemeContext);
  const [notifications, setNotifications] = useState("Email");
  const [language, setLanguage] = useState("English");

  const popoverContent = (
    <Menu className="user-profile-menu">
      <Menu.Item key="1" className="profile-item">
        <strong>See profile</strong>
      </Menu.Item>
      <Menu.Divider />
      <Menu.SubMenu key="2" title={`Theme: ${colorTheme === "light" ? "Light" : "Dark"}`}>
        <Menu.Item
          key="2-1"
          onClick={toggleTheme}
        >
          {colorTheme === "light" ? "Switch to Dark" : "Switch to Light"}
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.SubMenu key="3" title={`Notifications: ${notifications}`}>
        <Menu.Item key="3-1" onClick={() => setNotifications("Email")}>
          Email
        </Menu.Item>
        <Menu.Item key="3-2" onClick={() => setNotifications("After login")}>
          After login
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.SubMenu key="4" title={`Language: ${language}`}>
        <Menu.Item key="4-1" onClick={() => setLanguage("English")}>
          English
        </Menu.Item>
        <Menu.Item key="4-2" onClick={() => setLanguage("Español")}>
          Español
        </Menu.Item>
        <Menu.Item key="4-3" onClick={() => setLanguage("Français")}>
          Français
        </Menu.Item>
      </Menu.SubMenu>
      <Menu.Divider />
      <Menu.Item key="5" danger>
        Log out
      </Menu.Item>
    </Menu>
  );

  return (
    <>
      <Flex gap="large">
        <Link to="/">
          <Title
            style={{ marginTop: "0.5em" }}
            onClick={LaWikiClickHandler}
            className="header-title"
          >
            LaWiki
          </Title>
        </Link>
        <Title style={{ marginTop: "0.5em" }}>/</Title>
        <Title
          style={{ marginTop: "0.5em" }}
          onClick={WikiClickHandler}
          className="header-title"
        >
          JoJoWiki
        </Title>
      </Flex>

      <Flex gap={50}>
        <Input.Search
          placeholder="search for articles"
          allowClear
          suffix={FilterIcon()}
          size="large"
          style={{ width: "400px" }}
        />
        <Button
          variant="outlined"
          icon={AddIcon()}
          iconPosition="start"
          size={"large"}
        >
          New article
        </Button>
        <Badge count={9} size="large">
          <div className="icon-container" onClick={NotificationsClickHandler}>
            <BellOutlined style={{ fontSize: "24px" }} />
          </div>
        </Badge>
        <Popover
          content={popoverContent}
          trigger="click"
          placement="bottomRight"
          overlayStyle={{ width: 250 }}
        >
          <Avatar size="large" icon={<UserOutlined />}>
            A
          </Avatar>
        </Popover>
      </Flex>
    </>
  );
};

WikiHeader.propTypes = {
  children: PropTypes.node,
};

export default WikiHeader;
