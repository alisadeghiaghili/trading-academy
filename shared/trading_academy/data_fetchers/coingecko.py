"""CoinGecko data fetcher implementation."""

import asyncio
from datetime import datetime, timezone
from typing import List, Optional
import httpx
import pandas as pd

from shared.trading_academy.data_fetchers.base import BaseDataFetcher, OHLCV, TickerInfo, CacheMixin


class CoinGeckoFetcher(BaseDataFetcher, CacheMixin):
    """CoinGecko API data fetcher."""

    BASE_URL = "https://api.coingecko.com/api/v3"
    PRO_BASE_URL = "https://pro-api.coingecko.com/api/v3"

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        use_pro: bool = False,
        cache_dir: str = "data/cache/coingecko",
    ):
        """Initialize CoinGecko fetcher.

        Args:
            api_key: CoinGecko API key (for Pro).
            api_secret: Not used for CoinGecko.
            use_pro: Use Pro API.
            cache_dir: Cache directory.
        """
        BaseDataFetcher.__init__(self, api_key, api_secret)
        CacheMixin.__init__(self, cache_dir=cache_dir)

        self.use_pro = use_pro
        self.base_url = self.PRO_BASE_URL if use_pro else self.BASE_URL
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            headers = {}
            if self.api_key and self.use_pro:
                headers["x-cg-pro-api-key"] = self.api_key
            elif self.api_key:
                headers["x-cg-demo-api-key"] = self.api_key

            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
                headers=headers,
            )
        return self._client

    async def close(self) -> None:
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
        await super().close()

    def _get_coin_id(self, symbol: str) -> str:
        """Convert symbol to CoinGecko coin ID."""
        # Remove quote currency
        base = symbol.upper().split("/")[0].split("-")[0].split("_")[0]

        # Common mappings
        mapping = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "BNB": "binancecoin",
            "SOL": "solana",
            "ADA": "cardano",
            "XRP": "ripple",
            "DOT": "polkadot",
            "DOGE": "dogecoin",
            "AVAX": "avalanche-2",
            "MATIC": "polygon",
            "LINK": "chainlink",
            "UNI": "uniswap",
            "LTC": "litecoin",
            "BCH": "bitcoin-cash",
            "ATOM": "cosmos",
            "NEAR": "near",
            "FTM": "fantom",
            "ALGO": "algorand",
            "VET": "vechain",
            "ICP": "internet-computer",
            "FIL": "filecoin",
            "TRX": "tron",
            "ETC": "ethereum-classic",
            "XLM": "stellar",
            "THETA": "theta-token",
            "AAVE": "aave",
            "MKR": "maker",
            "COMP": "compound-governance-token",
            "SNX": "synthetix-network-token",
            "YFI": "yearn-finance",
            "SUSHI": "sushi",
            "CRV": "curve-dao-token",
            "1INCH": "1inch",
            "BAL": "balancer",
            "REN": "republic-protocol",
            "KNC": "kyber-network-crystal",
            "ZRX": "0x",
            "BAT": "basic-attention-token",
            "ENJ": "enjincoin",
            "MANA": "decentraland",
            "SAND": "the-sandbox",
            "AXS": "axie-infinity",
            "GALA": "gala",
            "CHZ": "chiliz",
            "HOT": "holo",
            "ZIL": "zilliqa",
            "ONT": "ontology",
            "QTUM": "qtum",
            "IOST": "iost",
            "NANO": "nano",
            "SC": "siacoin",
            "DGB": "digibyte",
            "RVN": "ravencoin",
            "DCR": "decred",
            "WAVES": "waves",
            "LSK": "lisk",
            "ARK": "ark",
            "STRAT": "stratis",
            "NXT": "nxt",
            "BCN": "bytecoin",
            "XMR": "monero",
            "XEM": "nem",
            "DASH": "dash",
            "ZEC": "zcash",
            "BTG": "bitcoin-gold",
            "ETC": "ethereum-classic",
            "BCH": "bitcoin-cash",
            "BSV": "bitcoin-cash-sv",
            "EOS": "eos",
            "TRX": "tron",
            "XTZ": "tezos",
            "NEO": "neo",
            "GAS": "gas",
            "ONT": "ontology",
            "ONG": "ong",
            "NAS": "nebulas",
            "ELF": "aelf",
            "AION": "aion",
            "WAN": "wanchain",
            "ICX": "icon",
            "QTUM": "qtum",
            "ZIL": "zilliqa",
            "THETA": "theta-token",
            "TFUEL": "theta-fuel",
            "BTT": "bittorrent",
            "WIN": "wink",
            "JST": "just",
            "SUN": "sun-token",
            "NFT": "apenft",
            "USDT": "tether",
            "USDC": "usd-coin",
            "BUSD": "binance-usd",
            "DAI": "dai",
            "TUSD": "true-usd",
            "USDP": "paxos-standard",
            "HUSD": "husd",
            "GUSD": "gemini-dollar",
            "FRAX": "frax",
            "LUSD": "liquity-usd",
            "MIM": "magic-internet-money",
            "ALUSD": "alusd",
            "FEI": "fei-usd",
            "RAI": "rai",
            "OHM": "olympus",
            "TIME": "wonderland",
            "SPELL": "spell-token",
            "MIMATIC": "mimatic",
            "ALPACA": "alpaca-finance",
            "ALPHA": "alpha-finance",
            "BAKE": "bakerytoken",
            "BURGER": "burger-swap",
            "CAKE": "pancakeswap-token",
            "COS": "contentos",
            "CREAM": "cream",
            "CTK": "certik",
            "CVP": "powerpool",
            "DEGO": "dego-finance",
            "DODO": "dodo",
            "DOT": "polkadot",
            "EGLD": "elrond-erd",
            "ENJ": "enjincoin",
            "FARM": "harvest-finance",
            "FIRO": "firo",
            "FLM": "flamingo-finance",
            "FOR": "for-tube",
            "FRONT": "frontier-token",
            "GRT": "the-graph",
            "HARD": "hard-protocol",
            "HNT": "helium",
            "ICP": "internet-computer",
            "IDEX": "idex",
            "INJ": "injective-protocol",
            "IOST": "iost",
            "IOTX": "iotex",
            "IRIS": "iris-network",
            "JST": "just",
            "KAVA": "kava",
            "KEEP": "keep-network",
            "KNC": "kyber-network-crystal",
            "KSM": "kusama",
            "LINA": "linear",
            "LIT": "litentry",
            "LRC": "loopring",
            "LTO": "lto-network",
            "MASK": "mask-network",
            "MATIC": "polygon",
            "MIR": "mirror-protocol",
            "NKN": "nkn",
            "NMR": "numeraire",
            "OCEAN": "ocean-protocol",
            "OGN": "origin-protocol",
            "OM": "mantra-dao",
            "ONE": "harmony",
            "ONG": "ong",
            "ORN": "orion-protocol",
            "OXT": "orchid-protocol",
            "PERP": "perpetual-protocol",
            "PHA": "phala-network",
            "PICKLE": "pickle-finance",
            "PNT": "pnetwork",
            "POLS": "polkastarter",
            "POLY": "polymath",
            "POND": "marlin",
            "PROM": "prometeus",
            "PUNDIX": "pundi-x",
            "QUICK": "quickswap",
            "RAMP": "ramp",
            "RAY": "raydium",
            "REN": "republic-protocol",
            "REP": "augur",
            "RLC": "iexec-rlc",
            "RPL": "rocket-pool",
            "RSR": "reserve-rights-token",
            "RUNE": "thorchain",
            "SAND": "the-sandbox",
            "SFI": "saffron-finance",
            "SKL": "skale",
            "SLP": "smooth-love-potion",
            "SNX": "synthetix-network-token",
            "SOL": "solana",
            "SRM": "serum",
            "STORJ": "storj",
            "STX": "blockstack",
            "SUSHI": "sushi",
            "SXP": "swipe",
            "TLM": "alien-worlds",
            "TKO": "tokocrypto",
            "TOMO": "tomochain",
            "TORN": "tornado-cash",
            "TRB": "tellor",
            "TRIBE": "tribe",
            "TROY": "troy",
            "TVK": "terra-virtua-kolect",
            "UMA": "uma",
            "UNFI": "unifi-protocol-dao",
            "UNI": "uniswap",
            "UTK": "utrust",
            "VET": "vechain",
            "VTHO": "vechain-thor-energy",
            "WAVES": "waves",
            "WAXP": "wax",
            "WING": "wing-finance",
            "WRX": "wazirx",
            "XLM": "stellar",
            "XMR": "monero",
            "XRP": "ripple",
            "XTZ": "tezos",
            "YFI": "yearn-finance",
            "YFII": "dfi-money",
            "ZEC": "zcash",
            "ZEN": "horizen",
            "ZIL": "zilliqa",
            "ZRX": "0x",
        }
        return mapping.get(base, base.lower())

    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1d",
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
    ) -> pd.DataFrame:
        """Fetch OHLCV data from CoinGecko (daily only for free tier)."""
        coin_id = self._get_coin_id(symbol)

        # CoinGecko free tier only supports daily data
        if timeframe != "1d":
            # For other timeframes, would need Pro or different source
            return pd.DataFrame()

        # Check cache
        cache_key = f"coingecko_{coin_id}_{timeframe}_{start}_{end}_{limit}"
        cached = self._load_from_cache(cache_key, max_age_hours=24)
        if cached is not None:
            return cached

        client = await self._get_client()

        # Determine days
        if start and end:
            days = (end - start).days
        else:
            days = min(limit, 365)  # Max 365 days for free

        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily" if days > 90 else "hourly",
        }

        try:
            response = await client.get(f"/coins/{coin_id}/market_chart", params=params)
            response.raise_for_status()
            data = response.json()

            if "prices" not in data:
                return pd.DataFrame()

            # CoinGecko returns [timestamp, price] arrays
            prices = data["prices"]
            volumes = data.get("total_volumes", [])
            market_caps = data.get("market_caps", [])

            # Build DataFrame
            df_data = []
            for i, (ts, price) in enumerate(prices):
                dt = datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                volume = volumes[i][1] if i < len(volumes) else 0
                market_cap = market_caps[i][1] if i < len(market_caps) else 0

                # For daily data, approximate OHLC from price
                df_data.append({
                    "timestamp": dt,
                    "open": price,
                    "high": price,
                    "low": price,
                    "close": price,
                    "volume": volume,
                    "market_cap": market_cap,
                })

            df = pd.DataFrame(df_data)
            df = df[["timestamp", "open", "high", "low", "close", "volume"]]

            # Cache
            self._save_to_cache(cache_key, df)

            return df

        except httpx.HTTPError as e:
            raise ConnectionError(f"CoinGecko API error: {e}")

    async def fetch_ohlcv_async(self, *args, **kwargs) -> pd.DataFrame:
        """Async alias."""
        return await self.fetch_ohlcv(*args, **kwargs)

    async def fetch_ticker(self, symbol: str) -> TickerInfo:
        """Fetch current ticker from CoinGecko."""
        coin_id = self._get_coin_id(symbol)
        client = await self._get_client()

        try:
            response = await client.get(
                "/simple/price",
                params={
                    "ids": coin_id,
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                    "include_24hr_vol": "true",
                    "include_market_cap": "true",
                }
            )
            response.raise_for_status()
            data = response.json()

            coin_data = data.get(coin_id, {})
            price = coin_data.get("usd", 0)
            change_24h_pct = coin_data.get("usd_24h_change", 0)
            volume_24h = coin_data.get("usd_24h_vol", 0)
            market_cap = coin_data.get("usd_market_cap")

            # Calculate absolute change
            change_24h = price * (change_24h_pct / 100) if price else 0

            return TickerInfo(
                symbol=symbol,
                name=symbol,
                price=price,
                change_24h=change_24h,
                change_24h_pct=change_24h_pct,
                volume_24h=volume_24h,
                market_cap=market_cap,
                last_updated=datetime.now(timezone.utc),
            )
        except httpx.HTTPError as e:
            raise ConnectionError(f"CoinGecko ticker error: {e}")

    async def fetch_symbols(self) -> List[str]:
        """Fetch supported coins from CoinGecko."""
        client = await self._get_client()

        try:
            response = await client.get("/coins/list")
            response.raise_for_status()
            coins = response.json()

            # Return symbols (would need mapping back)
            return [c["symbol"].upper() for c in coins]
        except httpx.HTTPError as e:
            raise ConnectionError(f"CoinGecko symbols error: {e}")

    async def fetch_global_data(self) -> dict:
        """Fetch global market data."""
        client = await self._get_client()

        try:
            response = await client.get("/global")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise ConnectionError(f"CoinGecko global data error: {e}")

    async def fetch_trending(self) -> List[dict]:
        """Fetch trending coins."""
        client = await self._get_client()

        try:
            response = await client.get("/search/trending")
            response.raise_for_status()
            data = response.json()
            return data.get("coins", [])
        except httpx.HTTPError as e:
            raise ConnectionError(f"CoinGecko trending error: {e}")


# Sync wrapper
class CoinGeckoFetcherSync:
    """Synchronous wrapper for CoinGeckoFetcher."""

    def __init__(self, *args, **kwargs):
        self._fetcher = CoinGeckoFetcher(*args, **kwargs)

    def fetch_ohlcv(self, *args, **kwargs) -> pd.DataFrame:
        return asyncio.run(self._fetcher.fetch_ohlcv(*args, **kwargs))

    def fetch_ticker(self, *args, **kwargs) -> TickerInfo:
        return asyncio.run(self._fetcher.fetch_ticker(*args, **kwargs))

    def fetch_symbols(self) -> List[str]:
        return asyncio.run(self._fetcher.fetch_symbols())

    def close(self):
        asyncio.run(self._fetcher.close())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()