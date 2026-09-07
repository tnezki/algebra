#!/usr/bin/env python3
from pathlib import Path
import hashlib, shutil, tempfile, sys

ROOT = Path.home() / "Documents" / "GitHub" / "algebra" / "banks" / "unit1"
EXPECTED = {'FINALIZATION_LOG.txt': 'cfda093b562ae77836d93a47d2dbe347ff6a2621', 'FULL_PIPELINE_AUDIT.json': 'b1992c89a5e1cb88f6e14b5fe3661c4555def338', 'ITEM_INDEX.json': '8c26edf0c330abd63b4b0ed459e0e731b4b68198', 'MAP_FIDELITY_REPORT.json': '343fb2b33502ef5ae9b80470b40277a4273c52a6', 'RENDER_QA_REPORT.json': 'd7b0b02fcb9f9c0b253651ff5e357efa165814db', 'V08_GRAPH_MODE_AUDIT.json': '3e3ba79d597dcddbc36dab259262c8e8f7560e6e', 'generate_graphs.py': 'acbab9ea033f2a5d9d3d2876a3afc0e16e9b73f3', 'seeds.json': '2a19c590cf52d800631414b576586568e37416fa', 'exit/section_1.1.json': '75b1b901383c06ad4c2618387adb15266c65a60f', 'exit/section_1.2.json': '71cbde332babf1be84cc14d3ef464e543fabfb7f', 'exit/section_1.3.json': '4fa5094a0bad0b79fcfa8d383844927acb004c9e', 'exit/section_1.4.json': '43759da9ed5f6a9ef81e50164a02d01c611a3b32', 'exit/section_1.5.json': '1a41d605e1e3578c7c4388da4730b40be34a104c', 'practice/section_1.1.json': '52233c0bbd98d592ea45a3a425d8b02a31604e79', 'practice/section_1.2.json': '50d64561fb023152bf28d930050dd377d3bf391a', 'practice/section_1.3.json': '8b41626ada565606372c69a6ec9545fed3793b66', 'practice/section_1.4.json': '66eb0f988b3e3ae858150b27aa5a340c305cc309', 'practice/section_1.5.json': 'c1452f397f5e243a4c2a183c49ae21a04cd53de0', 'summative/V1.json': 'e5274a8dc3a0e316458b48187b0ffbd847aff8b6', 'summative/V2.json': '7207f92ed2b9697573c11e07038daf9eb02381df', 'summative/V3.json': '9de99f23878683cc76f2117e3666b0c4f39b6176', 'summative/V4.json': '507cbbc07a8c5281da5097a273b4140116164c20', 'summative/V5.json': '6d562b80f3684c3688da9b48c0da2f9625c10878', 'summative/V6.json': '8abf1491145752fb8c32daee2ca15af220d49f09', 'wtc/section_1.1.json': '30fe5eee0ef071786e56a3dea044812afacba4db', 'wtc/section_1.2.json': '035f94130250cdef595b7237e0dd31ba050bc4ea', 'wtc/section_1.3.json': '3482b8b3ba64b2cd78a1d35a01288b8821e86525', 'wtc/section_1.4.json': 'fc7b308463a3309b5907a97695e7009675634be1', 'wtc/section_1.5.json': '4c5a57dbfa65ae15f91392b9230bd3f5d65df3d1', 'source_map/MAP_MANIFEST.json': 'eec08fee5c62ae086b28ec96f67c6a2044241f01', 'source_map/MAP_REPORT.txt': 'e148463300b194b370c7be873ff874480a9eb44d', 'source_map/bank_inventory_map.json': '30e827aa946c25e6830811a1ec0a56c852dedf35', 'source_map/exit_map.json': 'ad09b0fa5cd3f9735ba5f738c17a0cccbdfbb0f2', 'source_map/practice1_map.json': '865daaf20b5c4a9f8ffcf3ae5d6f61f500a4eb4f', 'source_map/seed_map.json': 'f8237d18c09ca53235eaf8f21e83b14b7ed91f14', 'source_map/summative_map.json': 'd1a5146b135b8caf7c5578d1364f67de7cc90954', 'source_map/unit1_question_design_map.json': 'a48a227093f157c864832a9b6c1825d1a6bdebfd', 'source_map/wtc_map.json': '936c692f1d36a0b84f4d2f233e515e3fecbada1f', 'figures/graph_0eea8d4d995a9803.png': 'aa4ec8d2828599a980c4338c5bc32c159408011b', 'figures/graph_4e1e110d72d922d7.png': '9aa892fb7c7680f5472fc0959a5b3c63ebd069ef', 'figures/graph_5bd598d25f939403.png': '896def4a88e472d6b6ed3637b0d238d554368fb6', 'figures/graph_81b6452d36666a5f.png': '03536e55e82d407e9129c3db97e284fa2d240d17', 'figures/graph_85b9bfa5a0dc334f.png': '91331de0c33cfea1a39e089a96f7b4d46ace7f92', 'figures/graph_926f822e3a6f7f15.png': '0ee159387e7c2d9b859b62836d8611b967bfe299', 'figures/graph_9345a2e50e5c173d.png': 'b8ff59b325018e869975e53c623fbd7cb0daac5b', 'figures/graph_a6efed5d7534b096.png': 'aa7088c98ce95e286f0463f6d1de4251bcf428d9', 'figures/graph_c0bd18cdacdbe9a1.png': 'bac28fc9d68f9ef301c23c534e2b8d47e79c482f', 'figures/graph_c8e7d169e88269d2.png': 'b43f4a0a80146912da3867d1f303aa25a02f7ac4', 'figures/graph_e204b25d5c3443cf.png': '92b0c39dadd6cee6877957231c0a2b54b43334c9', 'figures/graph_f78217870bbfe8cf.png': 'c0431e6c44cb0ee3d086302390fd531fd1e812fe', 'figures/graph_fd2639eafb995c62.png': '28c515fe47bd331e12559238cb7087ae4348e7bb', 'figures/u1sp_20260907_exit_1_1_q1_blank.png': '0d2b25852cfb405c28e83039a2a8c85a4f139413', 'figures/u1sp_20260907_exit_1_1_q2_scale.png': '7fa935ae40af6210534bb2de83f4fffa62732cdc', 'figures/u1sp_20260907_exit_1_1_q4_intercepts.png': 'e726e8081921e23f7d66494235c338247cc493bd', 'figures/u1sp_20260907_exit_1_2_q3_blank.png': '0d2b25852cfb405c28e83039a2a8c85a4f139413', 'figures/u1sp_20260907_exit_1_2_q4_scale.png': '24850cd0f0a79f08a11f5b067f8a5c52ce53c79b', 'figures/u1sp_20260907_exit_1_3_q1_rate.png': 'f285dbb8ea466201f710ce757d73c1b7c57985a4', 'figures/u1sp_20260907_exit_1_4_q1_scale.png': '7cd002c9be116fc35b0447d7e09f05f833b6b3b9', 'figures/u1sp_20260907_exit_1_4_q2_intercepts.png': '80094fae9010c7bbeda3a5a883a04cd060cfcabb', 'figures/u1sp_20260907_exit_1_4_q3_rate.png': 'cfab26be9e3f248982fb433fa0b5f8000f99c910', 'figures/u1sp_20260907_exit_1_5_q3_scale.png': 'ba0e57eaf02518377be8ff5834b6169dc45c298f', 'figures/u1sp_20260907_exit_1_5_q4_intercepts.png': '30daa5b0f839b2ec1ada89a447bef371388e15b4', 'figures/u1sp_20260907_practice_blank_number_line.png': '373d7c2590bde31b6c6c0cdcd35217996133151f', 'figures/u1sp_20260907_practice_blank_plane.png': '0d2b25852cfb405c28e83039a2a8c85a4f139413', 'figures/u1sp_20260907_practice_coord_a.png': '86ec666743b6d6579263de30e78bb12960909130', 'figures/u1sp_20260907_practice_coord_b.png': '7cd002c9be116fc35b0447d7e09f05f833b6b3b9', 'figures/u1sp_20260907_practice_coord_c.png': 'ca452e80ad9b99723460e5a604d88a73b582880d', 'figures/u1sp_20260907_practice_slope_b.png': '630fe89f088c7af7a756eb7bf916e80b739cae46', 'figures/u1sp_20260907_practice_slope_c.png': '96adaf05a4bed7c7645e0aff7f84a0c57d558580', 'figures/u1sp_20260907_summative_v1_mg01.png': 'fcbdd9b6e962b9452536043d1578ed575d536eb6', 'figures/u1sp_20260907_summative_v1_mg02.png': '4d744877b1c8a8751f198824b83b1220636ff26a', 'figures/u1sp_20260907_summative_v2_mg01.png': '66d9aa6ad50058e14d0337d6fd55c089064db5b4', 'figures/u1sp_20260907_summative_v2_mg02.png': 'f285dbb8ea466201f710ce757d73c1b7c57985a4', 'figures/u1sp_20260907_summative_v3_mg01.png': 'cb3c2d157253291d3015c196ceca1f7826752914', 'figures/u1sp_20260907_summative_v3_mg02.png': 'b022988c7e224c3da535959a2ef334a53bccc3a2', 'figures/u1sp_20260907_summative_v4_mg01.png': 'e726e8081921e23f7d66494235c338247cc493bd', 'figures/u1sp_20260907_summative_v4_mg02.png': 'ca452e80ad9b99723460e5a604d88a73b582880d', 'figures/u1sp_20260907_summative_v5_mg01.png': '96adaf05a4bed7c7645e0aff7f84a0c57d558580', 'figures/u1sp_20260907_summative_v5_mg02.png': '2b4f2d51d24092e3923e2a718990a324214385be', 'figures/u1sp_20260907_summative_v6_mg01.png': '481409397072b02733ca66e9b63d9b567dc1b923', 'figures/u1sp_20260907_summative_v6_mg02.png': '011ff18bb232ff83aca456050a3269d11de8e8ab', 'figures/u1sp_20260907_wtc_1_1_relationship.png': '7fa935ae40af6210534bb2de83f4fffa62732cdc'}
REMOVE_DIRS = ["exit", "practice", "summative", "wtc", "source_map"]
SELF = ROOT / "_finish_unit1_cleanup.py"

def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def main() -> int:
    if not ROOT.is_dir():
        print(f"FAIL: Unit 1 Bank folder not found: {ROOT}")
        return 2
    mismatches = []
    existing = []
    for rel, expected in EXPECTED.items():
        p = ROOT / rel
        if not p.exists():
            continue
        if not p.is_file():
            mismatches.append(f"{rel}: expected a file")
            continue
        actual = git_blob_sha1(p.read_bytes())
        if actual != expected:
            mismatches.append(f"{rel}: pinned {expected}, local {actual}")
        else:
            existing.append(rel)
    if mismatches:
        print("CLEANUP BLOCKED: one or more obsolete paths differ from the pinned canonical snapshot.")
        for item in mismatches:
            print(" -", item)
        print("No files were deleted.")
        return 2

    backup = Path(tempfile.mkdtemp(prefix="algebra_u1_cleanup_"))
    try:
        for rel in existing:
            src = ROOT / rel
            dst = backup / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        for rel in existing:
            (ROOT / rel).unlink()
        for rel in REMOVE_DIRS:
            d = ROOT / rel
            if d.exists() and d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        shutil.rmtree(backup)
        print(f"PASS: removed {len(existing)} obsolete Unit 1 Bank files after exact pinned-blob verification.")
        print("The new family Bank is now the only active Unit 1 Bank architecture.")
        try:
            SELF.unlink()
        except OSError:
            print(f"Cleanup succeeded; you may manually delete {SELF.name}.")
        return 0
    except Exception as exc:
        print("CLEANUP FAILED; restoring files from the temporary backup.")
        for src in backup.rglob("*"):
            if src.is_file():
                dst = ROOT / src.relative_to(backup)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        print("Restored backup. Error:", exc)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
