import { Flex, Typography, Spin, Row, Col, Button } from "antd";
const { Title } = Typography;
import { useSearchParams, useLocation, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useState, useEffect, useContext } from "react";

import { SettingsContext } from "../../../../context/settings-context";
import WikiCardGrid from "../../../wiki/components/wiki-card-grid/wiki-card-grid";
import WikiService from "../../../wiki/service/wiki-service";
const { searchWikisWithParams, searchWikisWithPaginationURL } = WikiService();

const UserWikis = ({
	author_name = "",
	order = "recent",
	search_limit = 6,
    active = true
}) => {
	const { t } = useTranslation();
	const { locale } = useContext(SettingsContext);
	const [searchParams, setSearchParams] = useSearchParams();
	const location = useLocation();
	const navigate = useNavigate();
	const pagination_url = location.state;

	const [loading, setLoading] = useState(true);

	const [wikis, setWikis] = useState([]);
	const [prevPageURL, setPrevPageURL] = useState(null);
	const [nextPageURL, setNextPageURL] = useState(null);
	const [currentPage, setCurrentPage] = useState(1);

	const [response, setResponse] = useState(null);

	const navigateToPage = (pagination_url, next_page) => {
		let newSearchParams = new URLSearchParams(location.search);
		newSearchParams.set("wiki_page", next_page);

		navigate(location.pathname + "?" + newSearchParams, {
			state: pagination_url,
		});
	};

	const updateState = (http_response) => {
		setResponse(http_response);
		setWikis(http_response.wikis);
		setPrevPageURL(http_response.previous);
		setNextPageURL(http_response.next);
	};

	const searchWikis = async () => {
		setLoading(true);
		try {
			const queryParams = retrieveSearchParams();

			var HTTPResponse;
			if (pagination_url != null) {
				HTTPResponse = await searchWikisWithPaginationURL(
					pagination_url,
					locale
				);
			} else {
				HTTPResponse = await searchWikisWithParams(queryParams);
			}

			updateState(HTTPResponse);

			if (searchParams.has("wiki_page"))
				setCurrentPage(Number(searchParams.get("wiki_page")));
		} catch (error) {
			console.error(error);
		} finally {
			setLoading(false);
		}
	};

	const retrieveSearchParams = () => {
		var queryParams = {
			offset: ((searchParams.get("wiki_page") || 1) - 1) * search_limit,
			limit: search_limit,
			order: order,
			author_name: author_name,
			lang: locale,
		};

		queryParams = Object.fromEntries(
			Object.entries(queryParams).filter(
				([_, value]) => value && value.length !== 0
			)
		);

		return queryParams;
	};

	useEffect(() => {
        console.log(active);
		setLoading(true);
		searchWikis();
	}, [searchParams, locale, active]);

	return (
		<Flex
			vertical
			align="center"
			style={{ width: "100%", marginBottom: 10 }}
		>
			{loading || response == null ? (
				<Spin size="large" style={{ paddingTop: "40vh" }} />
			) : (
				<>
					{!wikis?.length ? (
						<Title level={3}>{t("search.search-noresults")}</Title>
					) : (
						<>
							<WikiCardGrid wikiList={wikis} />

							<Row
								align="middle"
								justify="space-around"
								style={{ width: "80%", marginTop: 20 }}
								gutter={[16, 16]}
							>
								<Col xs={24} sm={8} align="center">
									<Button
										type="primary"
										disabled={prevPageURL == null}
										onClick={() =>
											navigateToPage(
												prevPageURL,
												currentPage - 1
											)
										}
									>
										{t("common.previous-page")}
									</Button>
								</Col>
								<Col xs={24} sm={8} align="center">
									{t("common.pagination", {
										page: currentPage,
										total: Math.ceil(
											response.total / response.limit
										),
									})}
								</Col>
								<Col xs={24} sm={8} align="center">
									<Button
										type="primary"
										disabled={nextPageURL == null}
										onClick={() =>
											navigateToPage(
												nextPageURL,
												currentPage + 1
											)
										}
									>
										{t("common.next-page")}
									</Button>
								</Col>
							</Row>
						</>
					)}
				</>
			)}
		</Flex>
	);
};

export default UserWikis;
