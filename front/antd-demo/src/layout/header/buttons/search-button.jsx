import { Button, Grid, Input } from "antd";
const { useBreakpoint } = Grid;
import { ControlOutlined } from "@ant-design/icons";

import { SearchIcon } from "../../../utils/icons";

const FilterClickHandler = () => {
    console.log("Filter clicked");
  }

const FilterIcon = () => {
    return (
      <div className="icon-container" onClick={FilterClickHandler}>
        <ControlOutlined style={{ fontSize: "24px" }} />
      </div>
    )
  }

const SearchButton = ({toggleHeader}) => {
  const screens = useBreakpoint();

  return (
    <>
      {screens.md ? (
        <Input.Search
        placeholder="search for articles"
        allowClear
        suffix={FilterIcon()}
        size="large"
        style={{ maxWidth: "300px" }}
      />
      ) : (
        <Button
          variant="outlined"
          icon={SearchIcon()}
          shape="circle"
          onClick={toggleHeader}
        />
      )}
    </>
  );
};

export default SearchButton;