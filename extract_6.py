import json
import os
import re

files = [
    '3_2_2_31_so_do_tuan_tu_huy_dat_phong.md',
    '3_2_2_32_so_do_tuan_tu_tao_tien_ich_moi.md',
    '3_2_2_33_so_do_tuan_tu_cap_nhat_tien_ich.md',
    '3_2_2_34_so_do_tuan_tu_xoa_tien_ich_he_thong.md',
    '3_2_2_35_so_do_tuan_tu_go_tien_ich_khoi_khach_san.md',
    '3_2_2_36_so_do_tuan_tu_go_tien_ich_khoi_phong.md',
    '3_2_2_so_do_tuan_tu.md',
    '3_2_3_01_so_do_hoat_dong_dang_nhap.md',
    '3_2_3_02_so_do_hoat_dong_dang_ky_tai_khoan.md',
    '3_2_3_03_so_do_hoat_dong_cap_nhat_thong_tin_ca_nhan.md',
    '3_2_3_04_so_do_hoat_dong_doi_mat_khau.md',
    '3_2_3_05_so_do_hoat_dong_xem_thong_tin_profile.md',
    '3_2_3_06_so_do_hoat_dong_xoa_tai_khoan_ca_nhan.md',
    '3_2_3_07_so_do_hoat_dong_xem_lich_su_dat_phong.md',
    '3_2_3_08_so_do_hoat_dong_xem_danh_sach_nguoi_dung.md',
    '3_2_3_09_so_do_hoat_dong_khoa_tai_khoan_nguoi_dung.md',
    '3_2_3_10_so_do_hoat_dong_mo_khoa_tai_khoan_nguoi_dung.md',
    '3_2_3_11_so_do_hoat_dong_them_phong_moi.md',
    '3_2_3_12_so_do_hoat_dong_cap_nhat_thong_tin_phong.md',
    '3_2_3_13_so_do_hoat_dong_xoa_phong.md'
]

dir_path = r'W:\Working\School\Y4_2\Luanvan\Report\Thesis\Hotel_Booking_PRD\thesis\chapters\03_thiet_ke\3_2_mo_hinh_xu_ly'
parent_dir = '3_2_mo_hinh_xu_ly'

nodes = []
edges = []
hyperedges = []

def make_id(stem, entity):
    s = f'{stem}_{entity}'.lower()
    return re.sub(r'[^a-z0-9_]', '_', s)

for f in files:
    full_path = os.path.join(dir_path, f)
    with open(full_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    stem = f'{parent_dir}_{os.path.splitext(f)[0]}'
    stem_id = make_id(parent_dir, os.path.splitext(f)[0])
    
    # parse yaml
    yaml_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    title = f
    dependencies = []
    author = None
    contributor = None
    
    if yaml_match:
        yaml_content = yaml_match.group(1)
        for line in yaml_content.split('\n'):
            if line.startswith('title:'):
                title = line.split(':', 1)[1].strip().strip('\"\'')
            if line.strip().startswith('-') and ('usecase' in line or 'so_do' in line or 'use_case' in line):
                dep = line.strip()[1:].strip().strip('\"\'')
                dependencies.append(dep)
            # handle case where dependencies is not list
            if line.startswith('dependencies:') and len(line.split(':', 1)) > 1:
                rest = line.split(':', 1)[1].strip()
                if rest and rest.endswith('.md'):
                    dependencies.append(rest)

    # create doc node
    doc_node_id = make_id(stem_id, 'doc')
    nodes.append({
        'id': doc_node_id,
        'label': title,
        'file_type': 'document',
        'source_file': f'thesis/chapters/03_thiet_ke/3_2_mo_hinh_xu_ly/{f}',
        'source_location': None,
        'source_url': None,
        'captured_at': None,
        'author': author,
        'contributor': contributor
    })
    
    # dependencies edges
    for dep in dependencies:
        dep_stem = make_id(parent_dir, os.path.splitext(dep)[0])
        dep_node_id = make_id(dep_stem, 'doc')
        edges.append({
            'source': doc_node_id,
            'target': dep_node_id,
            'relation': 'references',
            'confidence': 'EXTRACTED',
            'confidence_score': 1.0,
            'source_file': f'thesis/chapters/03_thiet_ke/3_2_mo_hinh_xu_ly/{f}',
            'source_location': None,
            'weight': 1.0
        })

    # parse plantuml components if any
    uml_match = re.search(r'```plantuml\n(.*?)\n```', content, re.DOTALL)
    if uml_match:
        uml = uml_match.group(1)
        components = set()
        
        # extract actors, boundaries, controls, entities
        for line in uml.split('\n'):
            line = line.strip()
            if line.startswith('actor '):
                components.add(line.split(' ')[1].strip('\"').split(' ')[0])
            elif line.startswith('boundary '):
                components.add(line.split(' ')[1].strip('\"').split(' ')[0])
            elif line.startswith('control '):
                components.add(line.split(' ')[1].strip('\"').split(' ')[0])
            elif line.startswith('entity '):
                components.add(line.split(' ')[1].strip('\"').split(' ')[0])
                
        for comp in components:
            if comp:
                comp_node_id = make_id(stem_id, comp)
                nodes.append({
                    'id': comp_node_id,
                    'label': comp,
                    'file_type': 'concept',
                    'source_file': f'thesis/chapters/03_thiet_ke/3_2_mo_hinh_xu_ly/{f}',
                    'source_location': None,
                    'source_url': None,
                    'captured_at': None,
                    'author': author,
                    'contributor': contributor
                })
                edges.append({
                    'source': doc_node_id,
                    'target': comp_node_id,
                    'relation': 'conceptually_related_to',
                    'confidence': 'EXTRACTED',
                    'confidence_score': 1.0,
                    'source_file': f'thesis/chapters/03_thiet_ke/3_2_mo_hinh_xu_ly/{f}',
                    'source_location': None,
                    'weight': 1.0
                })

out_json = {
    'nodes': nodes,
    'edges': edges,
    'hyperedges': hyperedges,
    'input_tokens': 0,
    'output_tokens': 0
}

with open(r'w:\Working\School\Y4_2\Luanvan\Report\Thesis\Hotel_Booking_PRD\graphify-out\.graphify_chunk_006.json', 'w', encoding='utf-8') as f:
    json.dump(out_json, f, ensure_ascii=False, indent=2)

print('Done')
