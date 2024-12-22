import { create } from 'zustand'
import deepEqual from "../utils/deepEqual";

const AddressesStore =
    // TODO: Добавть хендл ситуации с дублированием адресов
    create(set => (
            {Addresses: [],
            SetAddresses: addresses => set({ Addresses: addresses }),
            addAddress: (address) =>
                set((state) => {
                    if (!state.Addresses.some(item =>  deepEqual(item.properties, address.properties)) ) {
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