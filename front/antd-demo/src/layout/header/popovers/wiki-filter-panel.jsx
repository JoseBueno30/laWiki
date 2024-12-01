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
  const { t } = useTranslation("header");

  const orderOptions = [
    { label: t("order-recent"), value: "recent" },
    { label: t("order-oldest"), value: "oldest" },
    { label: t("order-popular"), value: "popular" },
    { label: t("order-unpopular"), value: "unpopular" },
  ];

  const updateOrder = (e) => {
    setFilters({ ...filters, order: e.target.value });
    console.log(filters.startDate, filters.endDate);
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

  return (
    <Flex vertical align="center">
      <Divider>{t("order-divider")}</Divider>
      <Radio.Group
        optionType="button"
        options={orderOptions}
        value={filters.order}
        onChange={updateOrder}
        block
      />
      <Divider>{t("daterange-divider")}</Divider>
      <RangePicker
        allowEmpty={[true, true]}
        value={[
          filters.startDate ? dayjs(filters.startDate, "YYYY/MM/DD") : null,
          filters.endDate ? dayjs(filters.endDate, "YYYY/MM/DD") : null,
        ]}
        onChange={updateDateRange}
        format={dateFormat}
      />
      <Divider>{t("author-divider")}</Divider>
      <Input
        defaultValue={filters.author}
        placeholder={t("author-placeholder")}
        allowClear
        onChange={updateAuthor}
        style={{ width: "80%" }}
      />
    </Flex>
  );
};

export default WikiFilterPanel;
