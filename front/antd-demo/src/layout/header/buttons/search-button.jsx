import { Button, Grid, Input } from "antd";
const { useBreakpoint } = Grid;

import { SearchIcon, FilterIcon } from "../../../utils/icons";
import IconWrapper from "../../../utils/icon-wrapper";
import Icon from "@ant-design/icons";

const FilterClickHandler = () => {
  console.log("Filter clicked");
};


const SearchButton = ({
  searchPlaceholder,
  filters,
  setFilters,
  query,
  setQuery,
  toggleHeader,
}) => {
  const screens = useBreakpoint();

  return (
    <>
      {screens.md ? (
        <Input.Search
          placeholder={searchPlaceholder}
          allowClear
          suffix={<IconWrapper icon={FilterIcon()} />}
          size="large"
          style={{ maxWidth: "300px" }}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
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
