import { Axios } from "./axios";
import { SEARCH_URL } from "./constants";


export type SearchRequest = {
    query: string;
    search_type: string;
}

export const getSearchResult = (searchRequest:SearchRequest) => {
    const params: any = {
        q: searchRequest.query,
        search_type: searchRequest.search_type,
    }
    
    return Axios().get(SEARCH_URL, { params });
};
