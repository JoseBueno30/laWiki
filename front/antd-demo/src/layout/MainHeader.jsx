import { Layout, Flex, Input, Button, Badge, Avatar } from "antd";
import {
  ControlOutlined,
  PlusOutlined,
  BellOutlined,
  UserOutlined,
} from "@ant-design/icons";
import PropTypes from "prop-types";
import "./PageHeader.css";
import Title from "antd/es/typography/Title";
import React from "react";

const FilterIcon = () => {
  return (
    <div className="icon-container" onClick={FilterClickHandler}>
      <ControlOutlined style={{ fontSize: "24px" }} />
    </div>
  )
}
const AddIcon = () => <PlusOutlined />;
const BellIcon = () => <BellOutlined />;

const ProfileClickHandler = () => {
  console.log("Profile clicked");
};

const NotificationsClickHandler = () => {
  console.log("Notifications clicked");
}

const FilterClickHandler = () => {
  console.log("Filter clicked");
}

const LaWikiClickHandler = () => {
  console.log("LaWiki clicked");
}

const MainHeader = ({ children }) => {
  return (
    <Layout className="app-layout">
      <Layout.Header className="app-header">
        <Flex gap='large'>
          <Title style={{ marginTop: "0.5em" }} onClick={LaWikiClickHandler} className="header-title">LaWiki</Title>
        </Flex>
        <Flex gap={50}>
          <Input.Search
            placeholder="search wikis"
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
            New Wiki
          </Button>
          <Badge count={9} size="large">
            <div className="icon-container" onClick={NotificationsClickHandler}>
            <BellOutlined style={{ fontSize: "24px" }} />
            </div>
          </Badge>
          <div className="icon-container" onClick={ProfileClickHandler}>
            <Avatar size="large" icon={<UserOutlined/>}/>
          </div>
        </Flex>
      </Layout.Header>
      <Layout.Content className="app-content">{children}</Layout.Content>
    </Layout>
  );
};

MainHeader.propTypes = {
  children: PropTypes.node,
};

export default MainHeader;
