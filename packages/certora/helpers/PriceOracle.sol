// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.0;

interface IPriceOracle  {
    /*
     * @param provider Contract providing the price feeds to use by the oracle
     * @param base Token to rate
     * @param quote Token used for the price rate
     */
    function getPrice(address provider, address base, address quote) external view returns (uint256);
}

contract PriceOracle is IPriceOracle {

    mapping(address => mapping(uint32 => uint256)) price;
    mapping(address => mapping(address => address)) feed;


    function getPrice(address, address base, address quote) public view override returns (uint256) {
        return _getPrice(feed[base][quote],uint32(block.timestamp));
    }

    function _getPrice(address _feed, uint32 time) internal view returns (uint256) {
        return price[_feed][time];
    }
}
