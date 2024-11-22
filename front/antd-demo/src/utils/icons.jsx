import React from 'react';
import { HomeOutlined, UserOutlined, SettingOutlined, PlusOutlined, SearchOutlined } from '@ant-design/icons';

const iconStyle = { color: 'var(--ant-primary-color)' };

export const HomeIcon = () => <HomeOutlined style={iconStyle} />;
export const UserIcon = () => <UserOutlined style={iconStyle} />;
export const SettingIcon = () => <SettingOutlined style={iconStyle} />;
export const AddIcon = () => <PlusOutlined style={iconStyle}/>;
export const SearchIcon = () => <SearchOutlined style={iconStyle}/>;