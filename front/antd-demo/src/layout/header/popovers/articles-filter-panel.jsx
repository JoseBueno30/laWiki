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
import { useContext } from "react";
import { SettingsContext } from "../../../context/settings-context";
dayjs.extend(customParseFormat);

const dateFormat = "YYYY/MM/DD";

const ArticlesFilterPanel = ({ filters, setFilters, wikiTags }) => {
  const { t } = useTranslation();
  const { locale } = useContext(SettingsContext);

  const orderOptions = [
    { label: t("common.order-recent"), value: "recent" },
    { label: t("common.order-oldest"), value: "oldest" },
    { label: t("common.order-popular"), value: "popular" },
    { label: t("common.order-unpopular"), value: "unpopular" },
  ];

  const updateOrder = (e) => {
    setFilters({ ...filters, order: e.target.value });
  };

  const removeTag = (tag) => {
    setFilters({ ...filters, tags: filters.tags.filter((t) => t !== tag) });
  };

  const addTag = (value) => {
    setFilters({ ...filters, tags: [...filters.tags, value] });
  };

  const updateDateRange = (dates) => {
    if (!dates) {
      setFilters({
        ...filters,
        startDate: null,
        endDate: null,
      });
      return;
    }

    const formattedDates = dates.map((date) =>
      date ? dayjs(date).format("YYYY/MM/DD") : null
    );
    setFilters({
      ...filters,
      startDate: formattedDates[0],
      endDate: formattedDates[1],
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
      <Divider>{t("common.order-header")}</Divider>
      <Radio.Group
        optionType="button"
        options={orderOptions}
        value={filters.order}
        onChange={updateOrder}
        block
      />
      <Divider>{t("common.tags-header")}</Divider>
      <Space wrap style={{ width: "100%" }}>
        {filters.tags.map((tag_id) => {
          // Busca en el wikiTags la tag con el id correspondiente
          const tag = wikiTags.find((tag) => tag.id === tag_id);
          return (
            <Tag key={tag_id} closable onClose={() => removeTag(tag_id)}>
              {tag.tag[locale]}
            </Tag>
          );
        })}
        <Select onChange={addTag} size="small" placeholder={t("tags-addtag")}>
          {wikiTags
            .filter((tag) => !filters.tags.includes(tag.id))
            .map((tag) => (
              <Select.Option key={tag.id} value={tag.id}>
                {tag.tag[locale]}
              </Select.Option>
            ))}
        </Select>
      </Space>
      <Divider>{t("common.daterange-header")}</Divider>
      <RangePicker
        allowEmpty={[true, true]}
        value={[
          filters.startDate ? dayjs(filters.startDate, "YYYY/MM/DD") : null,
          filters.endDate ? dayjs(filters.endDate, "YYYY/MM/DD") : null,
        ]}
        onChange={updateDateRange}
        format={dateFormat}
      />
      <Divider>{t("common.author-header")}</Divider>
      <Input
        defaultValue={filters.author}
        placeholder={t("common.author-placeholder")}
        allowClear
        onChange={updateAuthor}
        style={{ width: "80%" }}
      />
      <Divider>{t("common.editor-header")}</Divider>
      <Input
        defaultValue={filters.editor}
        placeholder={t("common.editor-placeholder")}
        allowClear
        onChange={updateEditor}
        style={{ width: "80%" }}
      />
    </Flex>
  );
};

export default ArticlesFilterPanel;
