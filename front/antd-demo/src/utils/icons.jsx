import React from "react";
import {
  HomeOutlined,
  UserOutlined,
  SettingOutlined,
  PlusOutlined,
  SearchOutlined,
  ControlOutlined,
} from "@ant-design/icons";

export const HomeIcon = () => <HomeOutlined />;
export const UserIcon = () => <UserOutlined />;
export const SettingIcon = () => <SettingOutlined />;
export const AddIcon = () => <PlusOutlined />;
export const SearchIcon = () => <SearchOutlined />;
export const FilterIcon = () => (
  <ControlOutlined style={{ fontSize: "24px" }} />
);
