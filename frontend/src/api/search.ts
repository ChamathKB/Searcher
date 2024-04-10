import { Axios } from "./axios";
import { SEARCH_URL } from "./constants";


export type SearchRequest = {
    query: string;
    search_type?: SearchType;
}

export const getSearchResult = (searchRequest:SearchRequest) => {
    const params: any = {
        q: searchRequest.query,
    }

    if (searchRequest.search_type) {
        params[searchRequest.search_type] = true;
    }
    
    return Axios().get(SEARCH_URL, { params });
};
