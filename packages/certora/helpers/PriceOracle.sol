// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.8.0;

import '@mimic-fi/v2-helpers/contracts/math/FixedPoint.sol';
interface IPriceOracle  {
    /*
     * @param provider Contract providing the price feeds to use by the oracle
     * @param base Token to rate
     * @param quote Token used for the price rate
     */
    function getPrice(address provider, address base, address quote) external view returns (uint256);
}

contract PriceOracle is IPriceOracle {
    using FixedPoint for uint256;

    mapping(address => mapping(uint32 => uint256)) private price;
    mapping(address => mapping(address => address)) private feed;

    function getPrice(address, address base, address quote) public view override returns (uint256) {
        return _getPrice(feed[base][quote],uint32(block.timestamp));
    }

    function _getPrice(address _feed, uint32 time) internal view returns (uint256) {
        return price[_feed][time];
    }

    function pow10(uint256 x) public pure returns (uint256) {
        require(x <= 77);
        return 10**x;
    }

    function uint32ToBytes4(uint32 x) public pure returns (bytes4) {
        return bytes4(x);
    }

    function mulDownFP(uint256 x, uint256 y) public pure returns (uint256) {
        return x.mulDown(y);
    }

    function getNativeBalanceOf(address account) public view returns (uint256) {
        return account.balance;
    }
}
