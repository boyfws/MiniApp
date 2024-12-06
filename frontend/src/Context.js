import { DefAddressProvider } from "./Contexts/DefAddressContext";
import { LoadingContextProvider } from "./Contexts/LoadingContext";
import { CategoriesContextProvider } from "./Contexts/CategoriesContext";

const ContextProvider = ({ children }) => {
    return (
        <LoadingContextProvider>
            <DefAddressProvider>
                <CategoriesContextProvider>
                    {children}
                </CategoriesContextProvider>
            </DefAddressProvider>
        </LoadingContextProvider>
    );
};

export {ContextProvider};