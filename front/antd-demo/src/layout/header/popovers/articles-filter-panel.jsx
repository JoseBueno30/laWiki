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
  import { useTranslation } from "react-i18next";
  import dayjs from "dayjs";
  import customParseFormat from "dayjs/plugin/customParseFormat";
  dayjs.extend(customParseFormat);
  
  const dateFormat = "YYYY/MM/DD";
  
  const ArticlesFilterPanel = ({ filters, setFilters, wikiTags }) => {
    const { t } = useTranslation('header');

    const orderOptions = [
      { label: t('order-recent'), value: "recent" },
      { label: t('order-oldest'), value: "oldest" },
      { label: t('order-popular'), value: "popular" },
      { label: t('order-unpopular'), value: "unpopular" },
    ];
    
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
  
    const updateDateRange = (_, dateStrings) => {
      setFilters({
        ...filters,
        startDate: dateStrings[0] ? dateStrings[0] : null,
        endDate: dateStrings[1] ? dateStrings[1]: null,
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
        <Divider>{t('order-divider')}</Divider>
        <Radio.Group
          optionType="button"
          options={orderOptions}
          value={filters.order}
          onChange={updateOrder}
          block
        />
        <Divider>{t('tags-divider')}</Divider>
        <Space wrap style={{ width: "100%" }}>
          {filters.tags.map((tag) => (
            <Tag key={tag} closable onClose={() => removeTag(tag)}>
              {tag}
            </Tag>
          ))}
          <Select
            onChange={addTag}
            size="small"
            placeholder={t('tags-addtag')}
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
        <Divider>{t('daterange-divider')}</Divider>
        <RangePicker
          value={[
            filters.startDate ? dayjs(filters.startDate, dateFormat) : null,
            filters.endDate ? dayjs(filters.endDate, dateFormat) : null,
          ]}
          onChange={updateDateRange}
        />
        <Divider>{t('author-divider')}</Divider>
        <Input
          defaultValue={filters.author}
          placeholder="author_name"
          allowClear
          onChange={updateAuthor}
          style={{ width: "80%" }}
        />
        <Divider>{t('editor-divider')}</Divider>
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
  