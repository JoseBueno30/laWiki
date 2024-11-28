import {
    Divider,
    Flex,
    Radio,
    Space,
    Tag,
    Select,
    DatePicker,
    Input,
  } from "antd";
  const { RangePicker } = DatePicker;
  import dayjs from "dayjs";
  import customParseFormat from "dayjs/plugin/customParseFormat";
  dayjs.extend(customParseFormat);
  
  const orderOptions = [
    { label: "Recent", value: "recent" },
    { label: "Oldest", value: "oldest" },
    { label: "Popular", value: "popular" },
    { label: "Unpopular", value: "unpopular" },
  ];
  
  const dateFormat = "YYYY/MM/DD";
  
  const ArticlesFilterPanel = ({ filters, setFilters, wikiTags }) => {
    const updateOrder = (e) => {
      setFilters({ ...filters, order: e.target.value });
    };
  
    const removeTag = (tag) => {
      setFilters({ ...filters, tags: filters.tags.filter((t) => t !== tag) });
    };
  
    const addTag = (value) => {
      setFilters({ ...filters, tags: [...filters.tags, value] });
      console.log(filters);
    };
  
    const updateDateRange = (dates) => {
      setFilters({
        ...filters,
        startDate: dates[0] ? dates[0].format(dateFormat) : null,
        endDate: dates[1] ? dates[1].format(dateFormat) : null,
      });
    };
  
    const updateAuthor = (e) => {
      setFilters({ ...filters, author: e.target.value });
    };
  
    const updateEditor = (e) => {
      setFilters({ ...filters, editor: e.target.value });
    };
  
    return (
      <Flex vertical align="center">
        <Divider>Order</Divider>
        <Radio.Group
          optionType="button"
          options={orderOptions}
          value={filters.order}
          onChange={updateOrder}
          wrap
        />
        <Divider>Tags</Divider>
        <Space wrap style={{ width: "100%" }}>
          {filters.tags.map((tag) => (
            <Tag key={tag} closable onClose={() => removeTag(tag)}>
              {tag}
            </Tag>
          ))}
          <Select
            onChange={addTag}
            style={{ width: "100px" }}
            size="small"
            defaultValue={"Add Tag"}
          >
            {wikiTags
              .filter((tag) => !filters.tags.includes(tag))
              .map((tag) => (
                <Select.Option key={tag} value={tag}>
                  {tag}
                </Select.Option>
              ))}
          </Select>
        </Space>
        <Divider>Date Range</Divider>
        <RangePicker
          value={[
            filters.startDate ? dayjs(filters.startDate, dateFormat) : null,
            filters.endDate ? dayjs(filters.endDate, dateFormat) : null,
          ]}
          onChange={updateDateRange}
        />
        <Divider>Author</Divider>
        <Input
          defaultValue={filters.author}
          placeholder="author_name"
          allowClear
          onChange={updateAuthor}
          style={{ width: "80%" }}
        />
        <Divider>Editor</Divider>
        <Input
          defaultValue={filters.editor}
          placeholder="editor_name"
          allowClear
          onChange={updateEditor}
          style={{ width: "80%" }}
        />
      </Flex>
    );
  };
  
  export default ArticlesFilterPanel;
  