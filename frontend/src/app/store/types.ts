export enum LoadingState {
    Loading = 'LOADING',
    Loaded = 'LOADED',
  }

export interface ProductState {
    state: LoadingState;
    data: Product[];
}

export interface SingleProductState {
    state: LoadingState;
    data?: SingleProduct;
}

export interface CartState {
    state: LoadingState;
    data: CartData
}

export interface CartData {  
    cart: Product[]   
}
export interface Product {
    id: number;
    name: string;
    quantity: number;
    price: number;
}

export interface SingleProduct {
    product: {
        id: number;
        name: string;
        price: number;
    } | undefined
    similar: SimilarProduct[];
}

export interface SimilarProduct {
    id: number;
    name: string;
    price: number;
}
