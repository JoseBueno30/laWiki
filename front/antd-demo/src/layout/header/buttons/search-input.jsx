import { Button, Grid, Input } from "antd";
const { useBreakpoint } = Grid;

import { SearchIcon } from "../../../utils/icons";

const SearchInput = ({
  searchPlaceholder,
  query,
  setQuery,
  toggleHeader,
  popover,
  searchFunction
}) => {

  const screens = useBreakpoint();

  return (
    <>
      {screens.md ? (
        <Input.Search
          placeholder={searchPlaceholder}
          allowClear
          suffix={popover}
          size="large"
          style={{ minWidth: "200px" }}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onSearch={searchFunction}
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

export default SearchInput;
