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
  
  const WikiFilterPanel = ({ filters, setFilters }) => {
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
          placeholder={t('author-placeholder')}
          allowClear
          onChange={updateAuthor}
          style={{ width: "80%" }}
        />
      </Flex>
    );
  };
  
  export default WikiFilterPanel;
  