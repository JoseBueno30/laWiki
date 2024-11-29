import { Button, Input, Space } from "antd";
import { CloseOutlined } from "@ant-design/icons";
import { FilterIcon } from "../../../utils/icons";

const CompactSearchInput = ({
    searchPlaceholder,
    query,
    setQuery,
    toggleHeader,
    popover,
    searchFunction
}) => {
  return (
    <Space.Compact style={{ width: "100%" }}>
      <Button
        size="large"
        icon={<CloseOutlined />}
        onClick={toggleHeader}
      />
      <Input.Search
        placeholder={searchPlaceholder}
        value={query}
        allowClear
        suffix={popover}
        size="large"
        onChange={(e) => setQuery(e.target.value)}
        onSearch={searchFunction}
      />
    </Space.Compact>
  );
};

export default CompactSearchInput;
