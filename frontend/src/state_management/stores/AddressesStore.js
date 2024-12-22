import { create } from 'zustand'
import CompareAddresses from "../../utils/CompareAddresses";

const AddressesStore =
    create(set => (
            {Addresses: [],
            SetAddresses: addresses => set({ Addresses: addresses }),
            addAddress: (address) =>
                set((state) => {
                    if (!state.Addresses.some(item =>  CompareAddresses(item.properties, address.properties)) ) {
                        return {
                            Addresses: [...state.Addresses, address],
                        };
                    }
                    return {
                        Addresses: [...state.Addresses]
                    };
                }),

            removeAddress: (address) =>
                set((state) => ({
                    Addresses: state.Addresses.filter((item) => item !== address),
                })),
            }
        )
    )


export default AddressesStore